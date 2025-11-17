# 🏥 MedAgentica - Multi-Agent Medical Assistant

<div align="center">

![MedAgentica Logo](assets/logo_rounded.png)

**🤖 Production-Ready AI Medical Assistant with Agentic RAG, Multi-Modal Analysis, and Beautiful React Frontend**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)

**🌟 Two Versions Available:**
- **Legacy Version**: `demo_agentic_rag.py` - Standalone Agentic RAG system (older version, no React frontend)
- **Modern Version**: React-based Neo-Aurora UI with full multi-agent capabilities (new version with React frontend)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Project Versions](#-project-versions)
- [🏗️ Architecture](#️-architecture)
- [🤖 Available Agents](#-available-agents)
- [🖼️ Medical Image Analysis](#️-medical-image-analysis)
- [📊 Evaluation Framework](#-evaluation-framework)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🔒 Security & Best Practices](#-security--best-practices)
- [🧪 Testing & Validation](#-testing--validation)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

**MedAgentica** is a state-of-the-art Multi-Agent Medical Assistant that combines the power of **Agentic RAG (Retrieval-Augmented Generation)**, **Medical Image Analysis**, and **Real-time Web Search** to provide accurate, evidence-based medical information and diagnostic support.

### What Makes This Special?

🎯 **Intelligent Agent Orchestration** - 7 specialized AI agents working in harmony  
🧠 **Self-Correcting RAG** - 4-agent workflow with reflection and re-retrieval  
🖼️ **Multi-Modal Analysis** - Brain MRI, Chest X-ray, and Skin Lesion detection  
🌐 **Real-time Research** - Latest medical information from PubMed and web  
🎨 **Beautiful UI** - Modern React frontend with Aurora theme  
⚡ **Production-Ready** - Comprehensive evaluation, error handling, and monitoring  
🔒 **Privacy-First** - Local image processing with optional cloud LLMs  

---

## ✨ Key Features

### 🤖 Agentic RAG System
**4-Agent Intelligent Workflow:**
1. **Query Analysis Agent** - Analyzes medical queries, extracts key terms, determines complexity
2. **Retrieval Agent** - Fetches relevant documents from vector database (Pinecone/ChromaDB)
3. **Reflection Agent** - Evaluates retrieval quality, decides if re-retrieval is needed
4. **Response Synthesis Agent** - Generates accurate, grounded responses with Chain-of-Thought reasoning

**Why It's Revolutionary:**
- ✅ **Self-Correcting** - Automatically improves retrieval if quality is low
- ✅ **Context-Aware** - Understands query intent and medical terminology
- ✅ **Hallucination Prevention** - Grounded responses with source attribution
- ✅ **Adaptive Retrieval** - Dynamically adjusts document count (3-10) based on query complexity

### 🩺 Medical Image Analysis

#### 🧠 Brain Tumor Detection
- **5-Class Classification**: No Tumor, Pituitary, Glioma, Meningioma, Other
- **MRI Segmentation**: Precise tumor localization
- **Follow-up Support**: Contextual answers to questions about analysis

#### 🫁 Chest X-Ray Analysis (MedRAX Integration)
- **18+ Disease Detection**: COVID-19, Pneumonia, Atelectasis, Cardiomegaly, Consolidation, Edema, Effusion, Emphysema, and more
- **Anatomical Segmentation**: 15+ structures (lungs, heart, spine, etc.)
- **Disease Grounding**: Visual localization with bounding boxes
- **Radiology Reports**: Professional Findings and Impression sections
- **Triple Output**: Original X-ray, Segmentation Overlay, Disease Grounding visualization

#### 🩺 Skin Lesion Classification
- **Binary Classification**: Benign vs Malignant
- **EfficientNet-B0 Model**: State-of-the-art deep learning
- **ABCDE Criteria**: Educational explanations about skin lesion characteristics
- **Professional Responses**: Doctor-style empathetic explanations

### 🌐 Neo-Aurora Web Interface

**Modern React Frontend** (`aurora-ai-main/`):
- 🌌 **Animated Aurora Background** - 3 floating orbs with dynamic grid
- 🎨 **Glassmorphism UI** - Frosted glass panels with layered depth
- 📊 **Live KPI Dashboard** - Real-time statistics (Active Agents, Queries Processed, Response Time, Success Rate)
- 🏷️ **Agent Badges** - Color-coded status indicators
- 📝 **Markdown Rendering** - Full markdown support with syntax highlighting
- 🖼️ **Image Handling** - Upload, preview, and full-screen modal view
- 📱 **Responsive Design** - Mobile-first approach
- ⌨️ **Keyboard Shortcuts** - Enhanced accessibility

### 📊 Comprehensive Evaluation Framework

**15+ Industry-Standard Metrics:**
- **Accuracy**: BLEU, ROUGE, Semantic Similarity
- **RAG Quality**: Faithfulness, Relevance, Hallucination Detection
- **Performance**: Latency (TTFT), Throughput, Memory Usage
- **Outputs**: Interactive HTML reports, Visualization charts, JSON data

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for React frontend)
- API Keys: Pinecone, Groq/OpenRouter (see Configuration)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Multi-Agent-Medical-Assistant.git
cd Multi-Agent-Medical-Assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# 5. Ingest medical documents (first time only)
python demo_ingest_pinecone.py
```

### Running the Application

#### Option 1: Modern React Frontend (Recommended)

```bash
# Terminal 1: Start backend server
python start_server.py
# Server runs on http://localhost:8001

# Terminal 2: Start React frontend
cd aurora-ai-main
npm install
npm run dev
# Frontend runs on http://localhost:8000
```

**Access**: Open http://localhost:8000 in your browser

#### Option 2: Legacy Standalone RAG System

```bash
# Run the demo agentic RAG system (older version, no React frontend)
python demo_ingest_pinecone.py  # First time only
python demo_agentic_rag.py
```

This runs the standalone Agentic RAG system without the React frontend. Perfect for:
- Testing RAG functionality
- Understanding the core system
- CLI-based interactions
- Integration into other applications

---

## 📦 Project Versions

This project contains **two versions** of the medical assistant:

### 1. **Legacy Version** - `demo_agentic_rag.py`
**Location**: Root directory  
**Type**: Standalone Python script  
**Frontend**: None (CLI-based)  
**Use Case**: 
- Testing Agentic RAG functionality
- Understanding core system architecture
- Integration into other Python applications
- Educational purposes

**How to Use:**
```bash
python demo_agentic_rag.py
```

**Features:**
- 4-Agent Agentic RAG workflow
- Query analysis, retrieval, reflection, and synthesis
- Self-correcting retrieval mechanism
- Source attribution and citations

### 2. **Modern Version** - React Frontend + FastAPI Backend
**Location**: 
- Frontend: `aurora-ai-main/`
- Backend: `web/app.py` and `start_server.py`

**Type**: Full-stack web application  
**Frontend**: React + TypeScript + Vite  
**Backend**: FastAPI (Python)  
**Use Case**:
- Production deployment
- User-friendly web interface
- Real-time multi-agent interactions
- Image upload and analysis
- Live KPI dashboard

**How to Use:**
```bash
# Start backend
python start_server.py

# Start frontend (in separate terminal)
cd aurora-ai-main
npm install
npm run dev
```

**Features:**
- Beautiful Neo-Aurora themed UI
- All 7 specialized agents
- Real-time image analysis
- Live statistics dashboard
- Markdown rendering
- Responsive design

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                         │
│         (React Frontend / CLI / API)                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              AGENT DECISION ROUTER                       │
│         (Intelligent Query Routing)                      │
└───┬──────┬──────┬──────┬──────┬──────┬──────┬──────────┘
    │      │      │      │      │      │      │
    ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│Conv │ │ RAG │ │ Web │ │Brain│ │Chest│ │Skin │ │Emerg│
│Agent│ │Agent│ │Srch │ │Tumor│ │Xray │ │Lesn │ │Resp │
└─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
```

### Agentic RAG Workflow

```
User Query
    ↓
┌─────────────────────┐
│ 1. Query Analysis   │ ← Analyzes intent, extracts terms
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 2. Retrieval        │ ← Searches Pinecone vector DB
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 3. Reflection       │ ← Evaluates quality
└──────────┬──────────┘
           ↓
    ┌──────────────┐
    │ Sufficient?  │
    └──┬───────┬───┘
   YES │       │ NO
       ↓       ↓
    ┌────┐  ┌──────────────┐
    │    │  │ Re-retrieve  │
    │    │  │ (refined)    │
    └─┬──┘  └──────┬───────┘
      │            │
      ↓            ↓
┌─────────────────────┐
│ 4. Response         │ ← Generates answer with CoT
│    Synthesis        │
└──────────┬──────────┘
           ↓
    Final Response
```

**Key Features:**
- **Chain of Thought**: Step-by-step reasoning
- **Self-Reflection**: Quality assessment & re-retrieval
- **Source Attribution**: Cites relevant documents
- **Context Grounding**: Prevents hallucinations

### Complete System Flow

See the detailed flowchart: [`assets/final-medical-assistant-flowchart-code.mermaid`](assets/final-medical-assistant-flowchart-code.mermaid)

**Visual Flowchart Available:**
- `assets/final_medical_assistant_flowchart.png`
- `assets/final_medical_assistant_flowchart_light.png`
- `assets/final_medical_assistant_flowchart_light_rounded.png`

---

## 🤖 Available Agents

### 💬 Conversation Agent
**Purpose**: General health discussions, greetings, casual chat  
**When to Use**: Non-medical questions, follow-up conversations  
**LLM**: Groq API (fast, 450 tokens/sec)

### 📚 RAG Agent (Agentic RAG System)
**Purpose**: Medical knowledge queries with document retrieval  
**When to Use**: Specific medical questions that can be answered from established literature  
**Knowledge Base**: 
- Introduction to brain tumors
- Deep learning techniques for brain tumor detection
- COVID-19 detection from chest X-rays
- And more...

**4-Agent Workflow:**
1. Query Analysis → 2. Retrieval → 3. Reflection → 4. Response Synthesis

### 🌐 Web Search Agent
**Purpose**: Latest medical research, current health news, time-sensitive information  
**When to Use**: Recent developments, current outbreaks, latest publications  
**Sources**: PubMed, Tavily Search, DuckDuckGo (fallback)  
**LLM**: OpenRouter API (free tier available)

### 🧠 Brain Tumor Agent
**Purpose**: Brain MRI analysis for tumor detection and segmentation  
**When to Use**: Upload brain MRI images  
**Capabilities**:
- 5-class classification
- Tumor segmentation
- Follow-up question support
**Model**: Local MedGemma (privacy-preserving)

### 🫁 Chest X-Ray Agent (MedRAX)
**Purpose**: Comprehensive chest X-ray analysis  
**When to Use**: Upload chest X-ray images  
**Capabilities**:
- 18+ disease classification
- Anatomical segmentation (15+ structures)
- Disease grounding with bounding boxes
- Professional radiology reports
**Model**: Local MedGemma + MedRAX integration

### 🩺 Skin Lesion Agent
**Purpose**: Skin condition analysis and classification  
**When to Use**: Upload skin lesion images  
**Capabilities**:
- Benign/Malignant classification
- ABCDE criteria explanation
- Professional medical explanations
**Model**: EfficientNet-B0 + Local MedGemma

### 🚨 Emergency Response Agent
**Purpose**: Critical medical emergencies requiring immediate attention  
**When to Use**: Chest pain, stroke symptoms, severe bleeding, difficulty breathing  
**Response**: Immediate guidance and emergency contact information

---

## 🖼️ Medical Image Analysis

### Supported Image Types

1. **Brain MRI** → Brain Tumor Agent
   - Formats: JPG, JPEG, PNG
   - Analysis: Tumor detection, classification, segmentation

2. **Chest X-Ray** → Chest X-Ray Agent
   - Formats: JPG, JPEG, PNG, DICOM
   - Analysis: 18+ diseases, anatomical segmentation, reports

3. **Skin Lesions** → Skin Lesion Agent
   - Formats: JPG, JPEG, PNG
   - Analysis: Benign/Malignant classification

### How It Works

```
Image Upload
    ↓
Image Classification (detects type)
    ↓
Route to Appropriate Agent
    ↓
Deep Learning Analysis
    ↓
Generate Report + Visualizations
    ↓
Return to User
```

### Privacy & Security

- ✅ **Local Processing**: Medical images processed locally using MedGemma
- ✅ **No Cloud Upload**: Images never leave your machine (for analysis)
- ✅ **Secure Storage**: Uploads stored in `uploads/` directory (gitignored)
- ✅ **Temporary Files**: Analysis results cleaned up automatically

---

## 📊 Evaluation Framework

### Quick Evaluation (3 minutes)

```bash
python evaluation/quick_evaluate.py
```

**Metrics:**
- Accuracy (BLEU, ROUGE, Semantic Similarity)
- RAG Quality (Faithfulness, Hallucination)
- Performance (Latency, Throughput)

### Comprehensive Evaluation (10 minutes)

```bash
python evaluation/evaluate_rag_llm.py
```

**Outputs:**
- `evaluation_results/evaluation_report_TIMESTAMP.html` - Interactive report
- `evaluation_results/evaluation_visualizations_TIMESTAMP.png` - Charts
- `evaluation_results/evaluation_results_TIMESTAMP.json` - Raw data

### Success Criteria

| Metric | Target | Good | Acceptable |
|--------|--------|------|------------|
| BLEU Score | > 0.7 | 0.5-0.7 | 0.3-0.5 |
| Hallucination | < 0.2 | 0.2-0.3 | 0.3-0.5 |
| Faithfulness | > 0.8 | 0.6-0.8 | 0.4-0.6 |
| Latency | < 2000ms | < 1500ms | 1500-3000ms |

---

## ⚙️ Configuration

### Required API Keys

Create a `.env` file in the root directory:

```bash
# Vector Database (Required)
PINECONE_API_KEY=pcsk_your_pinecone_key_here
PINECONE_INDEX_NAME=medagentica-demo-384

# LLM Provider (Choose one or more)
GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# OR
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1:free

# Optional Services
TAVILY_API_KEY=your_tavily_key  # Web search
ELEVEN_LABS_API_KEY=your_key    # Text-to-speech

# Local LLM (Optional - for image analysis)
USE_OLLAMA=true
OLLAMA_MODEL=alibayram/medgemma:4b
```

### Getting API Keys

1. **Pinecone** (Vector Database)
   - Sign up: https://app.pinecone.io/
   - Free tier: 1 index, 100k vectors
   - Get API key from dashboard

2. **Groq** (Fast LLM - Recommended)
   - Sign up: https://console.groq.com/
   - Free tier: 100k tokens/day
   - Fast inference: 450 tokens/sec

3. **OpenRouter** (Multiple Models)
   - Sign up: https://openrouter.ai/
   - Pay-per-use pricing
   - Free tier available

### Configuration File

Main configuration: `config.py`

**Key Settings:**
- LLM provider selection (Groq/OpenRouter/OpenAI/Ollama)
- Vector database selection (Pinecone/ChromaDB/Qdrant)
- Agent temperature settings
- Retrieval parameters
- Guardrails configuration

---

## 📁 Project Structure

```
Multi-Agent-Medical-Assistant/
│
├── 🚀 MAIN ENTRY POINTS
│   ├── demo_agentic_rag.py          # ⭐ Legacy: Standalone Agentic RAG (older version)
│   ├── start_server.py               # 🌐 Modern: Backend server starter
│   ├── launch.py                     # 🚀 Neo-Aurora launcher
│   └── web/app.py                    # 🌐 FastAPI backend
│
├── 🎨 FRONTEND (Modern Version)
│   └── aurora-ai-main/               # React + TypeScript frontend
│       ├── src/
│       │   ├── pages/Chat.tsx        # Main chat interface
│       │   └── components/           # UI components
│       └── package.json
│
├── 🧠 AGENTS (Core System)
│   ├── agent_decision.py             # Main routing agent
│   ├── rag_agent/                    # RAG System
│   │   ├── vectorstore_chroma.py
│   │   ├── vectorstore_qdrant.py
│   │   ├── content_processor.py
│   │   ├── doc_parser.py
│   │   ├── query_expander.py
│   │   ├── reranker.py
│   │   └── response_generator.py
│   ├── image_analysis_agent/         # Medical Image Analysis
│   │   ├── image_classifier.py
│   │   ├── brain_tumor_agent/
│   │   ├── chest_xray_agent/
│   │   └── skin_lesion_agent/
│   ├── web_search_processor_agent/   # Web Search
│   └── guardrails/                    # Safety & Validation
│
├── 📊 EVALUATION
│   ├── evaluation/
│   │   ├── quick_evaluate.py
│   │   ├── evaluate_rag_llm.py
│   │   └── check_evaluation_setup.py
│   └── evaluation_results/           # Generated reports (gitignored)
│
├── 🔧 CONFIGURATION
│   ├── config.py                     # System configuration
│   ├── .env.example                  # Template (copy to .env)
│   └── requirements.txt              # Python dependencies
│
├── 📚 DOCUMENTATION
│   ├── README.md                     # This file
│   ├── CHANGELOG.md                  # Version history
│   └── docs/                         # Additional docs
│
├── 🗄️ DATA (Not in Git)
│   ├── data/raw/                     # PDF documents
│   ├── data/chroma_db/               # ChromaDB storage
│   └── uploads/                      # User uploads
│
└── 🎨 ASSETS
    ├── logo_rounded.png
    ├── final_medical_assistant_flowchart.png
    └── *.mermaid                     # Flowchart source
```

---

## 🔒 Security & Best Practices

### ⚠️ Never Commit:

- `.env` - Your API keys!
- `data/` - Large datasets
- `uploads/` - User uploads
- `evaluation_results/` - Generated outputs
- `venv/` - Python environment
- `*.pth`, `*.h5` - Model weights

### ✅ Safe to Commit:

- `.env.example` - Template (no secrets)
- All `.py` and `.md` files
- `requirements.txt`
- `.gitignore`

### Security Features

- ✅ **Environment Variables**: All secrets in `.env` (gitignored)
- ✅ **Input Validation**: Guardrails for user inputs
- ✅ **Output Filtering**: Content moderation
- ✅ **Session Management**: Secure session handling
- ✅ **CORS Configuration**: Proper cross-origin settings
- ✅ **Local Image Processing**: Medical images processed locally

### Pre-Push Checklist

```bash
# 1. Check for secrets
grep -r "gsk_\|pcsk_\|sk-" . --exclude-dir=venv --exclude-dir=node_modules

# 2. Verify .gitignore
git status  # Should not show .env, data/, uploads/

# 3. Run tests
python evaluation/quick_evaluate.py

# 4. Check linter
# (if configured)
```

---
>>>>>>> 75e7a24 (docs: Consolidate documentation and update README)

## 🧪 Testing & Validation

### Quick Test

```bash
# Test backend health
curl http://localhost:8001/health

# Test chat endpoint
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}'
```

### Full Evaluation

```bash
# Comprehensive evaluation
python evaluation/evaluate_rag_llm.py

# View results
open evaluation_results/evaluation_report_*.html
```

### Unit Tests

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/
```

---

## 📚 Documentation

### Main Documentation

- **README.md** (this file) - Complete project overview
- **CHANGELOG.md** - Version history and updates

### Additional Resources

- **Architecture**: See `docs/ARCHITECTURE.txt` for detailed system design
- **Flowcharts**: Visual diagrams in `assets/` directory
- **Code Comments**: Comprehensive inline documentation

### Getting Help

1. Check this README first
2. Review `CHANGELOG.md` for recent changes
3. Check server logs: `tail -f server.log`
4. Open a GitHub issue for bugs or questions

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**: Run `python evaluation/quick_evaluate.py`
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Contribution Guidelines

- ✅ Follow existing code style
- ✅ Add tests for new features
- ✅ Update documentation
- ✅ Never commit `.env` or secrets
- ✅ Run evaluation before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Credits

Built with:

- 🦙 **LangChain** - RAG framework and agent orchestration
- 📌 **Pinecone** - Vector database for semantic search
- ⚡ **Groq** - Fast LLM inference
- 🤗 **HuggingFace** - Embeddings and models
- 🎨 **FastAPI** - Modern web framework
- ⚛️ **React** - Frontend framework
- 🎭 **MedRAX** - Chest X-ray analysis
- 🧠 **MedGemma** - Medical LLM for image analysis

---

## 🚀 Quick Commands Reference

```bash
# Legacy RAG System (older version, no React frontend)
python demo_agentic_rag.py

# Modern Full-Stack Application
python start_server.py              # Backend
cd aurora-ai-main && npm run dev    # Frontend

# Data Ingestion
python demo_ingest_pinecone.py

# Evaluation
python evaluation/quick_evaluate.py
python evaluation/evaluate_rag_llm.py

# Health Check
curl http://localhost:8001/health
```

---

## ⭐ Star This Repo

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**🌟 Made with ❤️ for the Medical AI Community 🌟**

[Documentation](README.md) | [Changelog](CHANGELOG.md) | [Issues](https://github.com/yourusername/Multi-Agent-Medical-Assistant/issues)

</div>
