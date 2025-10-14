"""
Agent Decision System for Multi-Agent Medical Chatbot

This module handles the orchestration of different agents using LangGraph.
It dynamically routes user queries to the appropriate agent based on content and context.
"""

import json
from typing import Dict, List, Optional, Any, Literal, TypedDict, Union, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import MessagesState, StateGraph, END
import os, getpass
from dotenv import load_dotenv
from agents.rag_agent import MedicalRAG
# Import the agentic RAG system
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from demo_agentic_rag import AgenticRAGSystem
from agents.web_search_processor_agent import WebSearchProcessorAgent
from agents.image_analysis_agent import ImageAnalysisAgent
from agents.guardrails.local_guardrails import LocalGuardrails

from langgraph.checkpoint.memory import MemorySaver

import cv2
import numpy as np

from config import Config

load_dotenv()

# Load configuration
config = Config()

# Initialize memory
memory = MemorySaver()

# Specify a thread
thread_config = {"configurable": {"thread_id": "1"}}


# Agent that takes the decision of routing the request further to correct task specific agent
class AgentConfig:
    """Configuration settings for the agent decision system."""
    
    # Decision model
    DECISION_MODEL = "gpt-4o"  # or whichever model you prefer

    # Vision model for image analysis
    VISION_MODEL = "gpt-4o"

    # Emergency keywords for immediate response
    EMERGENCY_KEYWORDS = [
        "chest pain", "heart attack", "stroke", "severe bleeding", "unconscious",
        "not breathing", "seizure", "overdose", "poisoning", "suicide",
        "severe allergic reaction", "anaphylaxis", "broken bone", "severe burn",
        "choking", "drowning", "electric shock", "head injury", "severe headache",
        "vision loss", "paralysis", "severe abdominal pain", "difficulty breathing"
    ]
    
    # Confidence threshold for responses
    CONFIDENCE_THRESHOLD = 0.85
    
    # System instructions for the decision agent
    DECISION_SYSTEM_PROMPT = """You are an intelligent medical triage system that routes user queries to
    the appropriate specialized agent. Your job is to analyze the user's request and determine which agent
    is best suited to handle it based on the query content, presence of images, and conversation context.

    Available agents:
    1. CONVERSATION_AGENT - For general chat, greetings, and non-medical questions.
    2. EMERGENCY_RESPONSE - For critical medical emergencies requiring immediate attention (chest pain, stroke, severe bleeding, etc.).
    3. RAG_AGENT - For specific medical knowledge questions that can be answered from established medical literature. Currently ingested medical knowledge involves 'introduction to brain tumor', 'deep learning techniques to diagnose and detect brain tumors', 'deep learning techniques to diagnose and detect covid / covid-19 from chest x-ray'.
    4. WEB_SEARCH_PROCESSOR_AGENT - For questions about recent medical developments, current outbreaks, or time-sensitive medical information.
    5. BRAIN_TUMOR_AGENT - For analysis of brain MRI images to detect and segment tumors.
    6. CHEST_XRAY_AGENT - For analysis of chest X-ray images to detect COVID-19 or other abnormalities.
    7. SKIN_LESION_AGENT - For analysis of skin lesion images to classify them as benign or malignant.

    **CRITICAL ROUTING RULES:**
    - **EMERGENCY FIRST**: If the user mentions emergency symptoms (chest pain, stroke, severe bleeding, difficulty breathing, etc.), route to EMERGENCY_RESPONSE immediately.
    - If an image is uploaded (has_image: true), PRIORITIZE MEDICAL IMAGE ANALYSIS AGENTS above all else.
    - If has_image: true AND image_type indicates a medical image, route to the appropriate medical vision agent IMMEDIATELY.
    - If the user mentions "analyze", "scan", "check", "diagnose", or "examine" with an uploaded image, route to the appropriate medical vision agent.
    - For text-only queries asking about medical knowledge, use RAG_AGENT.
    - For recent medical news or current events, use WEB_SEARCH_PROCESSOR_AGENT.
    - For general conversation without medical context, use CONVERSATION_AGENT.

    **MEDICAL IMAGE DETECTION:**
    - Chest X-ray images should go to CHEST_XRAY_AGENT for COVID-19 and abnormality detection.
    - Brain MRI images should go to BRAIN_TUMOR_AGENT for tumor detection and segmentation.
    - Skin lesion images should go to SKIN_LESION_AGENT for classification.
    - If image_type is unknown but user mentions medical analysis, default to CHEST_XRAY_AGENT.

    You must provide your answer in JSON format with the following structure:
    {{
    "agent": "AGENT_NAME",
    "reasoning": "Your step-by-step reasoning for selecting this agent",
    "confidence": 0.95  // Value between 0.0 and 1.0 indicating your confidence in this decision
    }}
    """

    # Initialize image analyzer
    image_analyzer = ImageAnalysisAgent(config=config)


class AgentState(MessagesState):
    """State maintained across the workflow."""
    # messages: List[BaseMessage]  # Conversation history
    agent_name: Optional[str]  # Current active agent
    current_input: Optional[Union[str, Dict]]  # Input to be processed
    has_image: bool  # Whether the current input contains an image
    image_type: Optional[str]  # Type of medical image if present
    output: Optional[str]  # Final output to user
    needs_human_validation: bool  # Whether human validation is required
    retrieval_confidence: float  # Confidence in retrieval (for RAG agent)
    bypass_routing: bool  # Flag to bypass agent routing for guardrails
    insufficient_info: bool  # Flag indicating RAG response has insufficient information


class AgentDecision(TypedDict):
    """Output structure for the decision agent."""
    agent: str
    reasoning: str
    confidence: float


def create_agent_graph():
    """Create and configure the LangGraph for agent orchestration."""

    # Initialize guardrails with the same LLM used elsewhere
    guardrails = LocalGuardrails(config.rag.llm)

    # LLM
    decision_model = config.agent_decision.llm
    
    # Initialize the output parser
    json_parser = JsonOutputParser(pydantic_object=AgentDecision)
    
    # Create the decision prompt
    decision_prompt = ChatPromptTemplate.from_messages([
        ("system", AgentConfig.DECISION_SYSTEM_PROMPT),
        ("human", "{input}")
    ])
    
    # Create the decision chain
    decision_chain = decision_prompt | decision_model | json_parser
    
    # Define graph state transformations
    def analyze_input(state: AgentState) -> AgentState:
        """Analyze the input to detect images and determine input type."""
        current_input = state["current_input"]
        has_image = False
        image_type = None
        
        # Get the text from the input
        input_text = ""
        if isinstance(current_input, str):
            input_text = current_input
        elif isinstance(current_input, dict):
            input_text = current_input.get("text", "")
        
        # Check input through guardrails if text is present
        if input_text:
            is_allowed, message = guardrails.check_input(input_text)
            if not is_allowed:
                # If input is blocked, return early with guardrail message
                print(f"Selected agent: INPUT GUARDRAILS, Message: ", message)
                return {
                    **state,
                    "messages": message,
                    "agent_name": "INPUT_GUARDRAILS",
                    "has_image": False,
                    "image_type": None,
                    "bypass_routing": True  # flag to end flow
                }
        
        # Original image processing code
        if isinstance(current_input, dict) and "image" in current_input:
            has_image = True
            image_path = current_input.get("image", None)
            image_type_response = AgentConfig.image_analyzer.analyze_image(image_path)
            # Handle both dict and string responses
            if isinstance(image_type_response, dict):
                image_type = image_type_response.get('image_type', 'unknown')
            else:
                image_type = str(image_type_response)
            print("ANALYZED IMAGE TYPE: ", image_type)
        
        return {
            **state,
            "has_image": has_image,
            "image_type": image_type,
            "bypass_routing": False  # Explicitly set to False for normal flow
        }
    
    def check_if_bypassing(state: AgentState) -> str:
        """Check if we should bypass normal routing due to guardrails."""
        if state.get("bypass_routing", False):
            return "apply_guardrails"
        return "route_to_agent"
    
    def route_to_agent(state: AgentState) -> Dict:
        """Make decision about which agent should handle the query."""
        messages = state["messages"]
        current_input = state["current_input"]
        has_image = state["has_image"]
        image_type = state["image_type"]

        # Check for emergency situations FIRST
        input_text = ""
        if isinstance(current_input, str):
            input_text = current_input.lower()
        elif isinstance(current_input, dict):
            input_text = current_input.get("text", "").lower()

        # Check if this is an emergency situation
        is_emergency = any(keyword in input_text for keyword in AgentConfig.EMERGENCY_KEYWORDS)

        if is_emergency:
            print("🚨 EMERGENCY SITUATION DETECTED in routing!")
            return {"agent_state": state, "next": "EMERGENCY_RESPONSE"}

        # Simple rule-based routing (no LLM needed for basic decisions)
        if has_image and image_type:
            # Route based on image type
            if "chest" in image_type.lower() or "x-ray" in image_type.lower() or "xray" in image_type.lower():
                print(f"Routing chest X-ray to CHEST_XRAY_AGENT")
                return {"agent_state": state, "next": "CHEST_XRAY_AGENT"}
            elif "brain" in image_type.lower() or "mri" in image_type.lower():
                print(f"Routing brain MRI to BRAIN_TUMOR_AGENT")
                return {"agent_state": state, "next": "BRAIN_TUMOR_AGENT"}
            elif "skin" in image_type.lower() or "lesion" in image_type.lower():
                print(f"Routing skin lesion to SKIN_LESION_AGENT")
                return {"agent_state": state, "next": "SKIN_LESION_AGENT"}
            else:
                # Unknown medical image, default to chest X-ray
                print(f"Routing unknown medical image to CHEST_XRAY_AGENT")
                return {"agent_state": state, "next": "CHEST_XRAY_AGENT"}

        # Text-based routing
        if any(keyword in input_text for keyword in ["web search", "latest", "recent", "news", "research", "current"]):
            print(f"Routing to WEB_SEARCH_PROCESSOR_AGENT")
            return {"agent_state": state, "next": "WEB_SEARCH_PROCESSOR_AGENT"}

        # Check for medical knowledge queries
        medical_keywords = ["symptom", "treatment", "diagnosis", "disease", "condition", "medicine", "medical"]
        if any(keyword in input_text for keyword in medical_keywords):
            print(f"Routing medical question to RAG_AGENT")
            return {"agent_state": state, "next": "RAG_AGENT"}

        # Default to conversation agent
        print(f"Routing to CONVERSATION_AGENT")
        return {"agent_state": state, "next": "CONVERSATION_AGENT"}

    # Define agent execution functions (these will be implemented in their respective modules)
    def run_conversation_agent(state: AgentState) -> AgentState:
        """Handle general conversation with emergency detection."""

        print(f"Selected agent: CONVERSATION_AGENT")

        messages = state["messages"]
        current_input = state["current_input"]

        # Check for emergency situations first
        input_text = ""
        if isinstance(current_input, str):
            input_text = current_input.lower()
        elif isinstance(current_input, dict):
            input_text = current_input.get("text", "").lower()

        # Check if this is an emergency situation
        is_emergency = any(keyword in input_text for keyword in AgentConfig.EMERGENCY_KEYWORDS)

        if is_emergency:
            print("🚨 EMERGENCY SITUATION DETECTED!")

            emergency_response = """🚨 **MEDICAL EMERGENCY DETECTED**

**IMMEDIATE ACTION REQUIRED:**

⚠️ **Call Emergency Services (911) immediately** if you are experiencing:
- Chest pain or heart attack symptoms
- Stroke symptoms (sudden weakness, speech difficulty, vision loss)
- Severe bleeding or injury
- Difficulty breathing or not breathing
- Seizures or convulsions
- Unconsciousness or confusion
- Severe allergic reactions

**What to do while waiting for help:**
• Stay calm and try to remain still
• If someone is with you, have them stay with you
• Do not drive yourself to the hospital
• Follow emergency operator instructions

**This is not a substitute for professional emergency medical care.**
**If this is a life-threatening emergency, call 911 NOW.**

Would you like me to help you find emergency contact information or provide guidance on what to tell the emergency operator?"""

            return {
                **state,
                "output": AIMessage(content=emergency_response),
                "agent_name": "EMERGENCY_RESPONSE"
            }

        # Create context from recent conversation history
        recent_context = ""
        for msg in messages:#[-20:]:  # Get last 10 exchanges (20 messages)  # currently considering complete history - limit control from config
            if isinstance(msg, HumanMessage):
                # print("######### DEBUG 1:", msg)
                recent_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                # print("######### DEBUG 2:", msg)
                recent_context += f"Assistant: {msg.content}\n"
        
        # Combine everything for the decision input
        conversation_prompt = f"""User query: {input_text}

        Recent conversation context: {recent_context}

        You are an AI-powered Medical Conversation Assistant. Your goal is to facilitate smooth and informative conversations with users, handling both casual and medical-related queries. You must respond naturally while ensuring medical accuracy and clarity.

        ### Role & Capabilities
        - Engage in **general conversation** while maintaining professionalism.
        - Answer **medical questions** using verified knowledge.
        - Route **complex queries** to RAG (retrieval-augmented generation) or web search if needed.
        - Handle **follow-up questions** while keeping track of conversation context.
        - Redirect **medical images** to the appropriate AI analysis agent.

        ### Guidelines for Responding:
        1. **General Conversations:**
        - If the user engages in casual talk (e.g., greetings, small talk), respond in a friendly, engaging manner.
        - Keep responses **concise and engaging**, unless a detailed answer is needed.

        2. **Medical Questions:**
        - If you have **high confidence** in answering, provide a medically accurate response.
        - Ensure responses are **clear, concise, and factual**.

        3. **Follow-Up & Clarifications:**
        - Maintain conversation history for better responses.
        - If a query is unclear, ask **follow-up questions** before answering.

        4. **Handling Medical Image Analysis:**
        - Do **not** attempt to analyze images yourself.
        - If user speaks about analyzing or processing or detecting or segmenting or classifying any disease from any image, ask the user to upload the image so that in the next turn it is routed to the appropriate medical vision agents.
        - If an image was uploaded, it would have been routed to the medical computer vision agents. Read the history to know about the diagnosis results and continue conversation if user asks anything regarding the diagnosis.
        - After processing, **help the user interpret the results**.

        5. **Uncertainty & Ethical Considerations:**
        - If unsure, **never assume** medical facts.
        - Recommend consulting a **licensed healthcare professional** for serious medical concerns.
        - Avoid providing **medical diagnoses** or **prescriptions**—stick to general knowledge.

        ### Response Format:
        - Maintain a **conversational yet professional tone**.
        - Use **bullet points or numbered lists** for clarity when needed.
        - If pulling from external sources (RAG/Web Search), mention **where the information is from** (e.g., "According to Mayo Clinic...").
        - If a user asks for a diagnosis, remind them to **seek medical consultation**.

        ### Example User Queries & Responses:

        **User:** "Hey, how's your day going?"
        **You:** "I'm here and ready to help! How can I assist you today?"

        **User:** "I have a headache and fever. What should I do?"
        **You:** "I'm not a doctor, but headaches and fever can have various causes, from infections to dehydration. If your symptoms persist, you should see a medical professional."

        Conversational LLM Response:"""

        # print("Conversation Prompt:", conversation_prompt)

        # Try to get response from LLM with fallback
        try:
            response = config.conversation.llm.invoke(conversation_prompt)
        except Exception as e:
            print(f"[Conversation Agent] LLM error: {e}")
            # Fallback response when LLM fails
            response = AIMessage(content=f"I'm here to help! You asked: '{input_text}'. For medical questions, I recommend consulting healthcare professionals. For general questions, I can provide helpful information when my services are available.")

        # response = AIMessage(content="This would be handled by the conversation agent.")

        return {
            **state,
            "output": response,
            "agent_name": "CONVERSATION_AGENT"
        }
    
    def run_rag_agent(state: AgentState) -> AgentState:
        """Handle medical knowledge queries using Agentic RAG System."""
        print(f"Selected agent: RAG_AGENT (Agentic RAG)")

        try:
            # Initialize the agentic RAG system
            agentic_rag = AgenticRAGSystem(
                pinecone_api_key=os.getenv("PINECONE_API_KEY", ""),
                pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", "medagentica"),
                openrouter_api_key=os.getenv("GROQ_API_KEY", ""),
                openrouter_model="llama-3.3-70b-versatile"
            )

            messages = state["messages"]
            query = state["current_input"]

            # Convert messages to chat history format for agentic RAG
            chat_history = []
            for msg in messages[-10:]:  # Last 5 exchanges
                if isinstance(msg, HumanMessage):
                    chat_history.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    chat_history.append({"role": "assistant", "content": msg.content})

            print(f"Processing query with Agentic RAG: {query[:100]}...")

            # Use the agentic RAG system
            response = agentic_rag.query(query, chat_history)

            response_text = response.get("response", "")
            confidence = response.get("confidence", 0.5)
            sources = response.get("sources", [])

            print(f"Agentic RAG Response preview: {response_text[:200]}...")
            print(f"Confidence: {confidence}")
            print(f"Sources found: {len(sources)}")

            # Check for insufficient information
            insufficient_info = (
                confidence < 0.3 or
                len(sources) == 0 or
                "don't have enough information" in response_text.lower() or
                "insufficient information" in response_text.lower()
            )

            print(f"Insufficient info flag: {insufficient_info}")

            # Determine if we should route to web search
            should_route_to_web_search = insufficient_info

            print(f"Should route to web search: {should_route_to_web_search}")

            # Store RAG output appropriately
            if should_route_to_web_search:
                response_output = AIMessage(content="")  # Empty response to trigger web search
            else:
                response_output = AIMessage(content=response_text)

            return {
                **state,
                "output": response_output,
                "needs_human_validation": False,
                "retrieval_confidence": confidence,
                "agent_name": "RAG_AGENT",
                "insufficient_info": insufficient_info
            }

        except Exception as e:
            print(f"Agentic RAG Agent Error: {e}")
            import traceback
            traceback.print_exc()

            # Return state that will trigger web search fallback
            return {
                **state,
                "output": AIMessage(content=""),
                "needs_human_validation": False,
                "retrieval_confidence": 0.0,
                "agent_name": "RAG_AGENT",
                "insufficient_info": True
            }

    # Web Search Processor Node
    def run_web_search_processor_agent(state: AgentState) -> AgentState:
        """Handles web search results, processes them with LLM, and generates a refined response."""

        print(f"Selected agent: WEB_SEARCH_PROCESSOR_AGENT")
        print("[WEB_SEARCH_PROCESSOR_AGENT] Processing Web Search Results...")
        
        messages = state["messages"]
        web_search_context_limit = config.web_search.context_limit

        recent_context = ""
        for msg in messages[-web_search_context_limit:]: # limit controlled from config
            if isinstance(msg, HumanMessage):
                # print("######### DEBUG 1:", msg)
                recent_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                # print("######### DEBUG 2:", msg)
                recent_context += f"Assistant: {msg.content}\n"

        web_search_processor = WebSearchProcessorAgent(config)

        processed_response = web_search_processor.process_web_search_results(query=state["current_input"], chat_history=recent_context)

        # print("######### DEBUG WEB SEARCH:", processed_response)
        
        if state['agent_name'] != None:
            involved_agents = f"{state['agent_name']}, WEB_SEARCH_PROCESSOR_AGENT"
        else:
            involved_agents = "WEB_SEARCH_PROCESSOR_AGENT"

        # Overwrite any previous output with the processed Web Search response
        return {
            **state,
            # "output": "This would be handled by the web search agent, finding the latest information.",
            "output": processed_response,
            "agent_name": involved_agents
        }

    # Define Routing Logic
    def confidence_based_routing(state: AgentState) -> str:
        """Route based on RAG confidence score and response content."""
        retrieval_confidence = state.get('retrieval_confidence', 0.0)
        insufficient_info = state.get('insufficient_info', False)
        
        print(f"Routing Decision:")
        print(f"  - Retrieval confidence: {retrieval_confidence}")
        print(f"  - Min confidence threshold: {config.rag.min_retrieval_confidence}")
        print(f"  - Insufficient info flag: {insufficient_info}")
        
        # Route to web search if confidence is low or info is insufficient
        if retrieval_confidence < config.rag.min_retrieval_confidence or insufficient_info:
            print("  - DECISION: Routing to WEB_SEARCH_PROCESSOR_AGENT")
            return "WEB_SEARCH_PROCESSOR_AGENT"
        else:
            print("  - DECISION: Proceeding with RAG response")
            return "check_validation"
    
    def run_brain_tumor_agent(state: AgentState) -> AgentState:
        """Handle brain MRI image analysis."""
        current_input = state["current_input"]
        image_path = current_input.get("image", None) if isinstance(current_input, dict) else None

        print(f"Selected agent: BRAIN_TUMOR_AGENT")
        print(f"Image path: {image_path}")

        if not image_path or not os.path.exists(image_path):
            response = AIMessage(content="Error: No valid brain MRI image provided for tumor analysis.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "BRAIN_TUMOR_AGENT"
            }

        try:
            # Use the brain tumor agent to analyze the image
            brain_tumor_result = AgentConfig.image_analyzer.classify_brain_tumor(image_path)
            print(f"Brain tumor analysis result: {brain_tumor_result}")

            response = AIMessage(content=brain_tumor_result)

            return {
                **state,
                "output": response,
                "needs_human_validation": False,  # Medical image analysis doesn't need validation
                "agent_name": "BRAIN_TUMOR_AGENT"
            }

        except Exception as e:
            print(f"Brain Tumor Agent Error: {e}")
            import traceback
            traceback.print_exc()

            response = AIMessage(content=f"Error analyzing brain MRI for tumors: {str(e)}. Please consult with a healthcare professional for proper evaluation.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "BRAIN_TUMOR_AGENT"
            }
    
    def run_chest_xray_agent(state: AgentState) -> AgentState:
        """Handle chest X-ray image analysis."""
        current_input = state["current_input"]
        image_path = current_input.get("image", None) if isinstance(current_input, dict) else None

        print(f"Selected agent: CHEST_XRAY_AGENT")
        print(f"Image path: {image_path}")

        if not image_path or not os.path.exists(image_path):
            response = AIMessage(content="Error: No valid image provided for chest X-ray analysis.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "CHEST_XRAY_AGENT"
            }

        try:
            # Classify chest x-ray into covid or normal using the trained model
            predicted_class = AgentConfig.image_analyzer.classify_chest_xray(image_path)
            print(f"Chest X-ray prediction: {predicted_class}")

            if predicted_class == "covid19":
                response = AIMessage(content="The analysis of the uploaded chest X-ray image indicates a **POSITIVE** result for **COVID-19**.")
            elif predicted_class == "normal":
                response = AIMessage(content="The analysis of the uploaded chest X-ray image indicates a **NEGATIVE** result for **COVID-19**, i.e., **NORMAL**.")
            else:
                response = AIMessage(content="The uploaded image could not be analyzed. Please ensure it's a clear chest X-ray image.")

            return {
                **state,
                "output": response,
                "needs_human_validation": False,  # Medical image analysis doesn't need validation
                "agent_name": "CHEST_XRAY_AGENT"
            }
            
        except Exception as e:
            print(f"Chest X-ray Agent Error: {e}")
            import traceback
            traceback.print_exc()
            
            response = AIMessage(content=f"Error analyzing chest X-ray: {str(e)}. Please try uploading a different image.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "CHEST_XRAY_AGENT"
            }

    def run_skin_lesion_agent(state: AgentState) -> AgentState:
        """Handle skin lesion image analysis."""
        current_input = state["current_input"]
        image_path = current_input.get("image", None) if isinstance(current_input, dict) else None

        print(f"Selected agent: SKIN_LESION_AGENT")
        print(f"Image path: {image_path}")

        if not image_path or not os.path.exists(image_path):
            response = AIMessage(content="Error: No valid image provided for skin lesion analysis.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "SKIN_LESION_AGENT"
            }

        try:
            # Segment skin lesion
            predicted_mask = AgentConfig.image_analyzer.segment_skin_lesion(image_path)
            print(f"Skin lesion segmentation result: {predicted_mask is not None}")

            if predicted_mask:
                # Check if overlay image was created
                overlay_path = AgentConfig.image_analyzer.skin_lesion_segmentation_output_path
                if os.path.exists(overlay_path):
                    response = AIMessage(content=f"""✅ **Skin Lesion Analysis Complete**

The uploaded skin lesion image has been successfully analyzed using AI segmentation technology.

**Analysis Results:**
• **Segmentation Status:** ✅ Successfully segmented
• **Visualization:** An overlay image showing the segmented lesion area has been generated
• **Clinical Note:** This AI analysis provides segmentation visualization for educational and preliminary assessment purposes

**Important Medical Disclaimer:**
This AI analysis is for informational purposes only and cannot replace professional medical evaluation. Please consult with a qualified dermatologist or healthcare professional for proper diagnosis and treatment recommendations.

**Next Steps:**
• Review the segmentation overlay image
• Consult with a healthcare professional for expert evaluation
• Consider follow-up examination if concerned about any skin changes""")
                else:
                    response = AIMessage(content="✅ **Skin Lesion Analysis Complete**\n\nThe skin lesion has been successfully segmented using AI technology. The segmentation overlay provides visual guidance for medical professionals to assess the lesion area.")
            else:
                response = AIMessage(content="❌ **Analysis Failed**\n\nThe uploaded image could not be properly analyzed. Please ensure:\n• The image shows a clear skin lesion\n• The image is well-lit and in focus\n• Try uploading a different image or consult with a healthcare professional.")

            return {
                **state,
                "output": response,
                "needs_human_validation": False,  # Medical image analysis doesn't need validation
                "agent_name": "SKIN_LESION_AGENT"
            }
            
        except Exception as e:
            print(f"Skin Lesion Agent Error: {e}")
            import traceback
            traceback.print_exc()
            
            response = AIMessage(content=f"Error analyzing skin lesion: {str(e)}. Please try uploading a different image.")
            return {
                **state,
                "output": response,
                "needs_human_validation": False,
                "agent_name": "SKIN_LESION_AGENT"
            }
    
    def handle_human_validation(state: AgentState) -> Dict:
        """Prepare for human validation if needed."""
        if state.get("needs_human_validation", False):
            return {"agent_state": state, "next": "human_validation", "agent": "HUMAN_VALIDATION"}
        return {"agent_state": state, "next": END}
    
    def perform_human_validation(state: AgentState) -> AgentState:
        """Handle human validation process."""
        print(f"Selected agent: HUMAN_VALIDATION")

        agent_name = state.get("agent_name", "")
        output_content = state['output'].content if hasattr(state['output'], 'content') else str(state['output'])

        # For medical image analysis agents, don't modify the response with validation prompts
        # Just mark that validation is needed but keep the original analysis
        medical_agents = ["CHEST_XRAY_AGENT", "BRAIN_TUMOR_AGENT", "SKIN_LESION_AGENT"]
        if any(m in agent_name for m in medical_agents):
            print(f"[Human Validation] Medical image analysis agent {agent_name} - keeping original response")
            return {
                **state,
                "output": state['output'],  # Keep original medical analysis response
                "agent_name": f"{state['agent_name']}, HUMAN_VALIDATION"
            }

        # For other agents, append validation request
        validation_prompt = f"{output_content}\n\n**Human Validation Required:**\n- If you're a healthcare professional: Please validate the output. Select **Yes** or **No**. If No, provide comments.\n- If you're a patient: Simply click Yes to confirm."

        # Create an AI message with the validation prompt
        validation_message = AIMessage(content=validation_prompt)

        return {
            **state,
            "output": validation_message,
            "agent_name": f"{state['agent_name']}, HUMAN_VALIDATION"
        }

    # Check output through guardrails
    def apply_output_guardrails(state: AgentState) -> AgentState:
        """Apply output guardrails to the generated response."""
        output = state["output"]
        current_input = state["current_input"]
        agent_name = state.get("agent_name", "")

        # Check if output is valid
        if not output or not isinstance(output, (str, AIMessage)):
            return state

        output_text = output if isinstance(output, str) else output.content

        # Skip guardrails for medical image analysis agents (substring match)
        medical_agents = ["CHEST_XRAY_AGENT", "BRAIN_TUMOR_AGENT", "SKIN_LESION_AGENT"]
        if any(m in agent_name for m in medical_agents):
            print(f"[Guardrails] Skipping output guardrails for medical image analysis agent: {agent_name}")
            # Ensure the assistant message is added to messages unchanged
            return {
                **state,
                "messages": output,
                "output": output
            }

        # If the last message was a human validation message
        if "Human Validation Required" in output_text:
            # Check if the current input is a human validation response
            validation_input = ""
            if isinstance(current_input, str):
                validation_input = current_input
            elif isinstance(current_input, dict):
                validation_input = current_input.get("text", "")

            # If validation input exists
            if validation_input.lower().startswith(('yes', 'no')):
                # Add the validation result to the conversation history
                validation_response = HumanMessage(content=f"Validation Result: {validation_input}")

                # If validation is 'No', modify the output
                if validation_input.lower().startswith('no'):
                    fallback_message = AIMessage(content="The previous medical analysis requires further review. A healthcare professional has flagged potential inaccuracies.")
                    return {
                        **state,
                        "messages": [validation_response, fallback_message],
                        "output": fallback_message
                    }

                return {
                    **state,
                    "messages": validation_response
                }

        # Get the original input text
        input_text = ""
        if isinstance(current_input, str):
            input_text = current_input
        elif isinstance(current_input, dict):
            input_text = current_input.get("text", "")

        # Apply output sanitization for non-medical agents
        sanitized_output = guardrails.check_output(output_text, input_text)

        # For non-validation cases, add the sanitized output to messages
        sanitized_message = AIMessage(content=sanitized_output) if isinstance(output, AIMessage) else sanitized_output

        return {
            **state,
            "messages": sanitized_message,
            "output": sanitized_message
        }

    
    # Create the workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes for each step
    workflow.add_node("analyze_input", analyze_input)
    workflow.add_node("route_to_agent", route_to_agent)
    workflow.add_node("CONVERSATION_AGENT", run_conversation_agent)
    workflow.add_node("EMERGENCY_RESPONSE", run_conversation_agent)  # Reuse conversation agent for emergencies
    workflow.add_node("RAG_AGENT", run_rag_agent)
    workflow.add_node("WEB_SEARCH_PROCESSOR_AGENT", run_web_search_processor_agent)
    workflow.add_node("BRAIN_TUMOR_AGENT", run_brain_tumor_agent)
    workflow.add_node("CHEST_XRAY_AGENT", run_chest_xray_agent)
    workflow.add_node("SKIN_LESION_AGENT", run_skin_lesion_agent)
    workflow.add_node("check_validation", handle_human_validation)
    workflow.add_node("human_validation", perform_human_validation)
    workflow.add_node("apply_guardrails", apply_output_guardrails)
    
    # Define the edges (workflow connections)
    workflow.set_entry_point("analyze_input")
    # workflow.add_edge("analyze_input", "route_to_agent")
    # Add conditional routing for guardrails bypass
    workflow.add_conditional_edges(
        "analyze_input",
        check_if_bypassing,
        {
            "apply_guardrails": "apply_guardrails",
            "route_to_agent": "route_to_agent"
        }
    )
    
    # Connect decision router to agents
    workflow.add_conditional_edges(
        "route_to_agent",
        lambda x: x["next"],
        {
            "CONVERSATION_AGENT": "CONVERSATION_AGENT",
            "EMERGENCY_RESPONSE": "EMERGENCY_RESPONSE",
            "RAG_AGENT": "RAG_AGENT",
            "WEB_SEARCH_PROCESSOR_AGENT": "WEB_SEARCH_PROCESSOR_AGENT",
            "BRAIN_TUMOR_AGENT": "BRAIN_TUMOR_AGENT",
            "CHEST_XRAY_AGENT": "CHEST_XRAY_AGENT",
            "SKIN_LESION_AGENT": "SKIN_LESION_AGENT",
            "needs_validation": "RAG_AGENT"  # Default to RAG if confidence is low
        }
    )
    
    # Connect agent outputs to validation check
    workflow.add_edge("CONVERSATION_AGENT", "check_validation")
    workflow.add_edge("EMERGENCY_RESPONSE", "check_validation")
    # workflow.add_edge("RAG_AGENT", "check_validation")
    workflow.add_edge("WEB_SEARCH_PROCESSOR_AGENT", "check_validation")
    workflow.add_conditional_edges("RAG_AGENT", confidence_based_routing)
    workflow.add_edge("BRAIN_TUMOR_AGENT", "check_validation")
    workflow.add_edge("CHEST_XRAY_AGENT", "check_validation")
    workflow.add_edge("SKIN_LESION_AGENT", "check_validation")

    workflow.add_edge("human_validation", "apply_guardrails")
    workflow.add_edge("apply_guardrails", END)
    
    workflow.add_conditional_edges(
        "check_validation",
        lambda x: x["next"],
        {
            "human_validation": "human_validation",
            END: "apply_guardrails"  # Route to guardrails instead of END
        }
    )
    
    # workflow.add_edge("human_validation", END)
    
    # Compile the graph
    return workflow.compile(checkpointer=memory)


def init_agent_state() -> AgentState:
    """Initialize the agent state with default values."""
    return {
        "messages": [],
        "agent_name": None,
        "current_input": None,
        "has_image": False,
        "image_type": None,
        "output": None,
        "needs_human_validation": False,
        "retrieval_confidence": 0.0,
        "bypass_routing": False,
        "insufficient_info": False
    }


def process_query(query: Union[str, Dict], conversation_history: List[BaseMessage] = None) -> str:
    """
    Process a user query through the agent decision system.
    
    Args:
        query: User input (text string or dict with text and image)
        conversation_history: Optional list of previous messages, NOT NEEDED ANYMORE since the state saves the conversation history now
        
    Returns:
        Response from the appropriate agent
    """
    # Initialize the graph
    graph = create_agent_graph()

    # # Save Graph Flowchart
    # image_bytes = graph.get_graph().draw_mermaid_png()
    # decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    # cv2.imwrite("./assets/graph.png", decoded)
    # print("Graph flowchart saved in assets.")
    
    # Initialize state
    state = init_agent_state()
    # if conversation_history:
    #     state["messages"] = conversation_history
    
    # Add the current query
    state["current_input"] = query

    # To handle image upload case
    if isinstance(query, dict):
        query = query.get("text", "") + ", user uploaded an image for diagnosis."
    
    state["messages"] = [HumanMessage(content=query)]

    # result = graph.invoke(state, thread_config)
    result = graph.invoke(state, thread_config)
    # print("######### DEBUG 4:", result)
    # state["messages"] = [result["messages"][-1].content]

    # Enhanced conversation memory management
    current_messages = result["messages"]

    # Keep history to reasonable size with intelligent summarization
    max_history = getattr(config, 'max_conversation_history', 20)

    if len(current_messages) > max_history:
        # Keep the most recent messages and summarize older ones if needed
        recent_messages = current_messages[-max_history:]

        # For very long conversations, add a summary message
        if len(current_messages) > max_history * 2:
            summary_message = AIMessage(content=f"💭 **Conversation Summary**: This is a continuation of our discussion about your health concerns. Previous topics included medical questions and responses. I'm here to help with any follow-up questions.")
            recent_messages.insert(0, summary_message)

        result["messages"] = recent_messages

    # visualize conversation history in console
    for m in result["messages"]:
        m.pretty_print()
    
    # Add the response to conversation history
    return result