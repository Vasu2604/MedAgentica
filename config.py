"""
Configuration file for the Multi-Agent Medical Chatbot

This file contains all the configuration parameters for the project.

If you want to change the LLM and Embedding model:

you can do it by changing all 'llm' and 'embedding_model' variables present in multiple classes below.

Each llm definition has unique temperature value relevant to the specific class. 
"""

import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI, OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_pinecone import Pinecone as PineconeVectorStore
from pinecone import Pinecone
import chromadb

# Load environment variables from .env file
load_dotenv()

def create_llm(temperature=0.7):
    """
    Create LLM instance based on configuration.
    Supports OpenRouter.ai (DeepSeek R1) and OpenAI.
    """
    # Check if OpenRouter is configured
    openrouter_api_key = os.getenv("openrouter_api_key")
    openrouter_model = os.getenv("openrouter_model", "deepseek/deepseek-chat-v3.1:free")
    
    if openrouter_api_key and openrouter_api_key != "YOUR_OPENROUTER_API_KEY":
        # Use OpenRouter.ai with DeepSeek R1
        return ChatOpenAI(
            model=openrouter_model,
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature
        )
    else:
        # Fallback to OpenAI or Azure OpenAI
        openai_api_key = os.getenv("openai_api_key")
        if openai_api_key and openai_api_key != "YOUR_OPENAI_API_KEY":
            return ChatOpenAI(
                model=os.getenv("openai_model", "gpt-4o"),
                api_key=openai_api_key,
                temperature=temperature
            )
        else:
            # Use Azure OpenAI as fallback
            return AzureChatOpenAI(
                deployment_name=os.getenv("deployment_name"),
                model_name=os.getenv("model_name", "gpt-4o"),
                azure_endpoint=os.getenv("azure_endpoint"),
                openai_api_key=os.getenv("openai_api_key"),
                openai_api_version=os.getenv("openai_api_version"),
                temperature=temperature
            )

def create_embedding_model():
    """
    Create embedding model based on configuration.
    Supports HuggingFace, OpenAI, and other providers.
    """
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
    
    if embedding_provider == "huggingface":
        # Use HuggingFace embeddings (free and reliable)
        return HuggingFaceEmbeddings(
            model_name=os.getenv("HUGGINGFACE_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        )
    elif embedding_provider == "openai":
        openai_embedding_key = os.getenv("OPENAI_EMBEDDING_API_KEY")
        if openai_embedding_key and openai_embedding_key != "YOUR_OPENAI_API_KEY":
            return OpenAIEmbeddings(
                api_key=openai_embedding_key,
                model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            )
        else:
            # Fallback to Azure OpenAI embeddings
            return AzureOpenAIEmbeddings(
                deployment=os.getenv("embedding_deployment_name"),
                model=os.getenv("embedding_model_name", "text-embedding-ada-002"),
                azure_endpoint=os.getenv("embedding_azure_endpoint"),
                openai_api_key=os.getenv("embedding_openai_api_key"),
                openai_api_version=os.getenv("embedding_openai_api_version")
            )
    else:
        # Default to HuggingFace embeddings (free and reliable)
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

def create_vectorstore(embedding_model, collection_name="medical_assistance_rag"):
    """
    Create vector store based on configuration.
    Supports Pinecone, ChromaDB, FAISS, and Qdrant.
    """
    vector_provider = os.getenv("VECTOR_STORE_PROVIDER", "pinecone").lower()
    
    if vector_provider == "pinecone":
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = os.getenv("PINECONE_INDEX_NAME", "medical-assistant-embeddings")
        
        # Get or create index
        try:
            existing_indexes = [index.name for index in pc.list_indexes()]
            if index_name not in existing_indexes:
                from pinecone import ServerlessSpec
                pc.create_index(
                    name=index_name,
                    dimension=384,  # sentence-transformers/all-MiniLM-L6-v2 dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
        except Exception as e:
            print(f"Warning: Could not create Pinecone index: {e}")
        
        return PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embedding_model
        )
    
    elif vector_provider == "chromadb":
        persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
        return Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=persist_directory
        )
    
    elif vector_provider == "faiss":
        persist_directory = os.getenv("FAISS_PERSIST_DIRECTORY", "./data/faiss_db")
        return FAISS.load_local(
            persist_directory,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    
    else:
        # Default to ChromaDB
        persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
        return Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=persist_directory
        )

class AgentDecisoinConfig:
    def __init__(self):
        self.llm = create_llm(temperature=0.1)  # Deterministic

class ConversationConfig:
    def __init__(self):
        self.llm = create_llm(temperature=0.7)  # Creative but factual

class WebSearchConfig:
    def __init__(self):
        self.llm = create_llm(temperature=0.3)  # Slightly creative but factual
        self.context_limit = 20     # include last 20 messsages (10 Q&A pairs) in history

class RAGConfig:
    def __init__(self):
        # Vector database configuration
        self.vector_db_type = os.getenv("EMBEDDING_PROVIDER", "chromadb").lower()
        self.embedding_dim = 1536  # Adjust based on your embedding model
        self.distance_metric = "Cosine"
        self.use_local = True
        self.vector_local_path = "./data/qdrant_db"  # Keep for Qdrant compatibility
        self.doc_local_path = "./data/docs_db"
        self.parsed_content_dir = "./data/parsed_docs"
        
        # Qdrant configuration (for backward compatibility)
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "medical_assistance_rag")
        
        # Document processing configuration
        self.chunk_size = 512
        self.chunk_overlap = 50
        
        # Initialize embedding model using the new helper function
        self.embedding_model = create_embedding_model()
        
        # Initialize LLM models using the new helper function
        self.llm = create_llm(temperature=0.3)  # Slightly creative but factual
        self.summarizer_model = create_llm(temperature=0.5)  # Slightly creative but factual
        self.chunker_model = create_llm(temperature=0.0)  # factual
        self.response_generator_model = create_llm(temperature=0.3)  # Slightly creative but factual
        self.top_k = 5
        self.vector_search_type = 'similarity'  # or 'mmr'

        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

        self.reranker_model = None  # Disabled due to authentication issues
        self.reranker_top_k = 3

        self.max_context_length = 8192  # (Change based on your need) # 1024 proved to be too low (retrieved content length > context length = no context added) in formatting context in response_generator code

        self.include_sources = True  # Show links to reference documents and images along with corresponding query response

        # ADJUST ACCORDING TO ASSISTANT'S BEHAVIOUR BASED ON THE DATA INGESTED:
        self.min_retrieval_confidence = 0.40  # The auto routing from RAG agent to WEB_SEARCH agent is dependent on this value

        self.context_limit = 20     # include last 20 messsages (10 Q&A pairs) in history
    
    def get_vectorstore(self):
        """
        Get or create vector store based on current configuration.
        """
        return create_vectorstore(self.embedding_model, self.collection_name)

class MedicalCVConfig:
    def __init__(self):
        self.brain_tumor_model_path = "./agents/image_analysis_agent/brain_tumor_agent/models/brain_tumor_segmentation.pth"
        self.chest_xray_model_path = "./agents/image_analysis_agent/chest_xray_agent/models/covid_chest_xray_model.pth"
        self.skin_lesion_model_path = "./agents/image_analysis_agent/skin_lesion_agent/models/checkpointN25_.pth.tar"
        self.skin_lesion_segmentation_output_path = "./uploads/skin_lesion_output/segmentation_plot.png"
        self.llm = create_llm(temperature=0.1)  # Keep deterministic for classification tasks

class SpeechConfig:
    def __init__(self):
        self.eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")  # Replace with your actual key
        self.eleven_labs_voice_id = "21m00Tcm4TlvDq8ikWAM"    # Default voice ID (Rachel)

class ValidationConfig:
    def __init__(self):
        self.require_validation = {
            "CONVERSATION_AGENT": False,
            "RAG_AGENT": False,
            "WEB_SEARCH_AGENT": False,
            "BRAIN_TUMOR_AGENT": True,
            "CHEST_XRAY_AGENT": True,
            "SKIN_LESION_AGENT": True
        }
        self.validation_timeout = 300
        self.default_action = "reject"

class APIConfig:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 8000
        self.debug = True
        self.rate_limit = 10
        self.max_image_upload_size = 5  # max upload size in MB

class UIConfig:
    def __init__(self):
        self.theme = "light"
        # self.max_chat_history = 50
        self.enable_speech = True
        self.enable_image_upload = True

class Config:
    def __init__(self):
        self.agent_decision = AgentDecisoinConfig()
        self.conversation = ConversationConfig()
        self.rag = RAGConfig()
        self.medical_cv = MedicalCVConfig()
        self.web_search = WebSearchConfig()
        self.api = APIConfig()
        self.speech = SpeechConfig()
        self.validation = ValidationConfig()
        self.ui = UIConfig()
        self.eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.max_conversation_history = 20  # Include last 20 messsages (10 Q&A pairs) in history

# # Example usage
# config = Config()