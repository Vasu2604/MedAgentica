# Multi-Agent Medical Assistant - Setup Guide

## Overview
This guide will help you configure the Multi-Agent Medical Assistant to use:
- **OpenRouter.ai** with **DeepSeek R1** model for LLM
- **Multiple embedding options**: Pinecone, ChromaDB, or FAISS
- **Flexible vector database** support

## Prerequisites
- Python 3.8+
- OpenRouter.ai API key
- Pinecone API key (if using Pinecone)
- OpenAI API key (if using OpenAI embeddings)

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Create your `.env` file** in the project root directory with the following content:

## Environment Configuration

### Step 1: Create `.env` file

Create a `.env` file in your project root with the following content:

```env
# =============================================================================
# LLM Configuration - OpenRouter.ai (DeepSeek R1)
# =============================================================================
# OpenRouter.ai Configuration
openrouter_api_key=YOUR_ACTUAL_OPENROUTER_API_KEY
openrouter_base_url=https://openrouter.ai/api/v1
openrouter_model=deepseek/deepseek-v3.1

# Alternative: If you want to use OpenAI directly (uncomment and fill)
# openai_api_key=YOUR_OPENAI_API_KEY
# openai_base_url=https://api.openai.com/v1
# openai_model=gpt-4o

# =============================================================================
# Embedding Configuration - Multiple Options
# =============================================================================

# Option 1: Pinecone (Recommended for production)
# Uncomment and configure if using Pinecone
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
PINECONE_ENVIRONMENT=YOUR_PINECONE_ENVIRONMENT
PINECONE_INDEX_NAME=medical-assistant-embeddings
EMBEDDING_PROVIDER=pinecone

# Option 2: ChromaDB (Good for local development)
# Uncomment if using ChromaDB
# CHROMA_PERSIST_DIRECTORY=./data/chroma_db
# EMBEDDING_PROVIDER=chromadb

# Option 3: FAISS (Good for local development)
# Uncomment if using FAISS
# FAISS_PERSIST_DIRECTORY=./data/faiss_db
# EMBEDDING_PROVIDER=faiss

# Option 4: OpenAI Embeddings (if you have OpenAI API key)
# Uncomment if using OpenAI embeddings
# OPENAI_EMBEDDING_API_KEY=YOUR_OPENAI_API_KEY
# OPENAI_EMBEDDING_MODEL=text-embedding-3-small
# EMBEDDING_PROVIDER=openai

# Default embedding provider (change to: pinecone, chromadb, faiss, or openai)
# EMBEDDING_PROVIDER=pinecone

# =============================================================================
# Vector Database Configuration
# =============================================================================
# Qdrant Configuration (if using Qdrant)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=medical_assistance_rag

# =============================================================================
# External API Keys
# =============================================================================
# Eleven Labs for Speech
ELEVEN_LABS_API_KEY=YOUR_ELEVEN_LABS_API_KEY

# Tavily for Web Search
TAVILY_API_KEY=YOUR_TAVILY_API_KEY

# Hugging Face (for reranker)
HUGGINGFACE_TOKEN=YOUR_HUGGINGFACE_TOKEN

# =============================================================================
# Application Configuration
# =============================================================================
# Environment
ENVIRONMENT=development
DEBUG=True

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# File Upload Limits
MAX_UPLOAD_SIZE_MB=5

# =============================================================================
# Legacy Azure OpenAI Configuration (Keep for compatibility)
# =============================================================================
# These are kept for backward compatibility but won't be used with OpenRouter
deployment_name=
model_name=gpt-4o
azure_endpoint=
openai_api_key=YOUR_OPENAI_API_KEY
openai_api_version=

# Embedding Model Configuration (Legacy)
embedding_deployment_name=
embedding_model_name=text-embedding-ada-002
embedding_azure_endpoint=
embedding_openai_api_key=YOUR_OPENAI_API_KEY
embedding_openai_api_version=
```

### Step 2: Configure Your API Keys

Replace the following placeholders with your actual API keys:

1. **OpenRouter.ai API Key**:
   - Get your API key from [OpenRouter.ai](https://openrouter.ai/)
   - Replace `YOUR_ACTUAL_OPENROUTER_API_KEY` with your key

2. **Pinecone API Key** (if using Pinecone):
   - Get your API key from [Pinecone](https://www.pinecone.io/)
   - Replace `YOUR_PINECONE_API_KEY` with your key
   - Set your environment (e.g., `us-east-1-aws`)

3. **OpenAI API Key** (if using OpenAI embeddings):
   - Get your API key from [OpenAI](https://platform.openai.com/)
   - Replace `YOUR_OPENAI_API_KEY` with your key

### Step 3: Choose Your Embedding Provider

Uncomment and configure ONE of the following options:

#### Option A: Pinecone (Recommended for Production)
```env
PINECONE_API_KEY=your_actual_pinecone_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=medical-assistant-embeddings
EMBEDDING_PROVIDER=pinecone
```

#### Option B: ChromaDB (Good for Local Development)
```env
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
EMBEDDING_PROVIDER=chromadb
```

#### Option C: FAISS (Good for Local Development)
```env
FAISS_PERSIST_DIRECTORY=./data/faiss_db
EMBEDDING_PROVIDER=faiss
```

#### Option D: OpenAI Embeddings
```env
OPENAI_EMBEDDING_API_KEY=your_openai_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_PROVIDER=openai
```

## Configuration Details

### LLM Configuration
The system now supports:
- **OpenRouter.ai** with DeepSeek R1 model (primary)
- **OpenAI** GPT models (fallback)
- **Azure OpenAI** (legacy fallback)

### Embedding Models
- **OpenAI**: `text-embedding-3-small`, `text-embedding-ada-002`
- **HuggingFace**: `sentence-transformers/all-MiniLM-L6-v2`
- **Custom**: Any compatible embedding model

### Vector Databases
- **Pinecone**: Cloud-based, scalable, production-ready
- **ChromaDB**: Local, good for development
- **FAISS**: Local, fast similarity search
- **Qdrant**: Local/cloud, feature-rich

## Usage Examples

### Using Pinecone
```python
from config import Config

config = Config()
# Automatically uses Pinecone if configured in .env
vectorstore = config.rag.get_vectorstore()
```

### Using ChromaDB
```python
from config import Config

config = Config()
# Automatically uses ChromaDB if configured in .env
vectorstore = config.rag.get_vectorstore()
```

### Using OpenRouter.ai
```python
from config import create_llm

# Creates DeepSeek R1 model via OpenRouter.ai
llm = create_llm(temperature=0.7)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Verify your API keys are correct and have proper permissions.

3. **Vector Store Issues**: Ensure the specified directories exist and are writable.

4. **Model Not Found**: Check that the model name is correct for your provider.

### Testing Configuration

You can test your configuration by running:

```python
from config import create_llm, create_embedding_model, create_vectorstore

# Test LLM
llm = create_llm()
print("LLM created successfully:", llm.model_name)

# Test embedding model
embedding_model = create_embedding_model()
print("Embedding model created successfully")

# Test vector store
vectorstore = create_vectorstore(embedding_model)
print("Vector store created successfully")
```

## Migration from Azure OpenAI

If you're migrating from Azure OpenAI:

1. Keep the legacy configuration in `.env` for backward compatibility
2. Add the new OpenRouter.ai configuration
3. The system will automatically use OpenRouter.ai when configured
4. Gradually migrate other components as needed

## Support

For issues or questions:
1. Check the configuration examples above
2. Verify your API keys and permissions
3. Check the logs for specific error messages
4. Ensure all dependencies are properly installed
