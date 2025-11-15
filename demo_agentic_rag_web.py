"""
Modern Web Interface for Agentic RAG System

A beautiful, modern web UI for the Agentic RAG system with:
- Sidebar with conversation history
- Clean chat interface
- Real-time streaming responses
- Professional design

Usage:
    python demo_agentic_rag_web.py
    
Then open http://localhost:8001 in your browser
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from demo_agentic_rag import AgenticRAGSystem

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Agentic RAG Web Interface")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversations in memory (in production, use a database)
conversations: Dict[str, List[Dict]] = {}
conversation_titles: Dict[str, str] = {}

# Initialize RAG system
rag_system = None


def initialize_rag_system():
    """Initialize the Agentic RAG system."""
    global rag_system
    
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medagentica")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    if not PINECONE_API_KEY or not GROQ_API_KEY:
        raise ValueError("Please set PINECONE_API_KEY and GROQ_API_KEY in .env file")
    
    rag_system = AgenticRAGSystem(
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_index_name=PINECONE_INDEX_NAME,
        openrouter_api_key=GROQ_API_KEY,
        openrouter_model=GROQ_MODEL
    )
    print("✅ Agentic RAG System initialized!")


# Pydantic models
class ChatMessage(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class NewConversationResponse(BaseModel):
    conversation_id: str
    title: str


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    try:
        initialize_rag_system()
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize RAG system: {e}")
        print("   Please check your .env file and ensure API keys are set")


@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the main HTML page."""
    html_path = Path(__file__).parent / "demo_rag_ui.html"
    
    if not html_path.exists():
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error: demo_rag_ui.html not found</h1>
            <p>Please ensure demo_rag_ui.html is in the same directory as this script.</p>
        </body>
        </html>
        """, status_code=500)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())


@app.get("/api/conversations")
async def get_conversations():
    """Get all conversation titles."""
    return {
        "conversations": [
            {
                "id": conv_id,
                "title": conversation_titles.get(conv_id, "New Conversation"),
                "last_updated": conversations[conv_id][-1]["timestamp"] if conversations.get(conv_id) else datetime.now().isoformat()
            }
            for conv_id in sorted(conversations.keys(), reverse=True)
        ]
    }


@app.post("/api/conversations/new", response_model=NewConversationResponse)
async def create_new_conversation():
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = []
    conversation_titles[conversation_id] = "New Conversation"
    
    return NewConversationResponse(
        conversation_id=conversation_id,
        title="New Conversation"
    )


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get messages for a specific conversation."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "title": conversation_titles.get(conversation_id, "New Conversation"),
        "messages": conversations[conversation_id]
    }


@app.delete("/api/conversations")
async def clear_all_conversations():
    """Clear all conversations."""
    global conversations, conversation_titles
    conversations = {}
    conversation_titles = {}
    return {"message": "All conversations cleared"}


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Handle chat messages."""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    # Create new conversation if needed
    conversation_id = message.conversation_id
    if not conversation_id or conversation_id not in conversations:
        conversation_id = str(uuid.uuid4())
        conversations[conversation_id] = []
        # Generate title from first message (first 50 chars)
        title = message.message[:50] + "..." if len(message.message) > 50 else message.message
        conversation_titles[conversation_id] = title
    
    # Add user message
    user_message = {
        "role": "user",
        "content": message.message,
        "timestamp": datetime.now().isoformat()
    }
    conversations[conversation_id].append(user_message)
    
    # Get chat history
    chat_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversations[conversation_id][:-1]
    ]
    
    try:
        # Query RAG system
        response = rag_system.query(
            user_query=message.message,
            chat_history=chat_history if chat_history else None,
            max_reflection_iterations=2
        )
        
        # Add assistant message
        assistant_message = {
            "role": "assistant",
            "content": response['response'],
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "confidence": response.get('confidence', 0),
                "doc_count": response.get('retrieved_doc_count', 0),
                "sources": response.get('sources', []),
                "query_type": response.get('query_analysis', {}).get('query_type', 'N/A'),
                "complexity": response.get('query_analysis', {}).get('complexity', 'N/A')
            }
        }
        conversations[conversation_id].append(assistant_message)
        
        return {
            "conversation_id": conversation_id,
            "message": assistant_message
        }
        
    except Exception as e:
        error_message = {
            "role": "assistant",
            "content": f"I apologize, but I encountered an error while processing your question: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "error": True
        }
        conversations[conversation_id].append(error_message)
        
        return {
            "conversation_id": conversation_id,
            "message": error_message
        }


@app.post("/api/regenerate")
async def regenerate_response(conversation_id: str):
    """Regenerate the last response."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if len(conversations[conversation_id]) < 2:
        raise HTTPException(status_code=400, detail="No message to regenerate")
    
    # Remove last assistant message
    conversations[conversation_id].pop()
    
    # Get the last user message
    last_user_message = conversations[conversation_id][-1]["content"]
    
    # Get chat history (excluding the last user message)
    chat_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversations[conversation_id][:-1]
    ]
    
    try:
        # Query RAG system again
        response = rag_system.query(
            user_query=last_user_message,
            chat_history=chat_history if chat_history else None,
            max_reflection_iterations=2
        )
        
        # Add new assistant message
        assistant_message = {
            "role": "assistant",
            "content": response['response'],
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "confidence": response.get('confidence', 0),
                "doc_count": response.get('retrieved_doc_count', 0),
                "sources": response.get('sources', []),
                "query_type": response.get('query_analysis', {}).get('query_type', 'N/A'),
                "complexity": response.get('query_analysis', {}).get('complexity', 'N/A')
            }
        }
        conversations[conversation_id].append(assistant_message)
        
        return {
            "conversation_id": conversation_id,
            "message": assistant_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏥 AGENTIC RAG SYSTEM - Modern Web Interface")
    print("="*80 + "\n")
    print("🚀 Starting server...")
    print("📱 Open http://localhost:8001 in your browser")
    print("="*80 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )

