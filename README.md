# 🏥 Multi-Agent Medical Assistant with Agentic RAG

> **Production-ready Medical AI system with advanced Agentic RAG, comprehensive evaluation framework, and multi-modal capabilities**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Clone & Install
git clone <your-repo-url>
cd Multi-Agent-Medical-Assistant
pip install -r requirements.txt

# 2. Configure API Keys
cp .env.example .env
# Edit .env with your API keys (Pinecone, Groq/OpenRouter)

# 3. Ingest Medical Documents
python demo_ingest_pinecone.py

# 4. Run Agentic RAG System
python demo_agentic_rag.py

# 5. Evaluate Performance
python quick_evaluate.py
```

**Done! Your medical AI is running!** 🎉

---

## ⭐ Main Features

### 🤖 **Agentic RAG System** (`demo_agentic_rag.py`)
**Primary entry point** - Advanced multi-agent RAG with self-reflection

**4-Agent Workflow**:
1. **Query Analysis Agent** - Analyzes medical queries intelligently
2. **Retrieval Agent** - Fetches relevant documents from Pinecone
3. **Reflection Agent** - Evaluates retrieval quality & decides if re-retrieval needed
4. **Response Synthesis Agent** - Generates accurate, grounded responses

**Why it's special**:
- ✅ Self-correcting retrieval
- ✅ Context-aware responses
- ✅ Hallucination prevention
- ✅ Source attribution

### 📊 **Comprehensive Evaluation Framework**
**Industry-standard metrics** for RAG & LLM systems

**15+ Metrics**:
- **Accuracy**: BLEU, ROUGE, Semantic Similarity
- **RAG Quality**: Faithfulness, Relevance, Hallucination Detection
- **Performance**: Latency (TTFT), Throughput, Memory Usage

**Outputs**:
- Interactive HTML reports
- Visualization charts
- JSON data for analysis

### 🩺 **Medical Image Analysis**
- **Brain Tumor Detection** - MRI segmentation and classification
- **Chest X-Ray Analysis** - 18+ disease detection (COVID-19, Pneumonia, Atelectasis, etc.)
- **Skin Lesion Classification** - Benign vs Malignant classification with ABCDE criteria

### 🌐 **Neo-Aurora Web Interface**
- **Beautiful Aurora Theme** - Animated background with floating orbs
- **Glassmorphism UI** - Modern frosted glass design
- **Real-time KPI Dashboard** - Live statistics (Active Agents, Queries, Response Time, Success Rate)
- **Multi-Agent Chat** - Color-coded agent badges and intelligent routing
- **Image Upload & Analysis** - Drag & drop, preview, and full-screen modal
- **Markdown Support** - Rich text rendering with syntax highlighting

---

## 📁 Project Structure

```
📂 Main Entry Points
├── demo_agentic_rag.py       ⭐ PRIMARY: Agentic RAG System
├── app.py                     🌐 Web Application
└── quick_evaluate.py          📊 Quick Evaluation

📂 Setup & Configuration
├── .env.example              🔒 Template (copy to .env)
├── config.py                 ⚙️  System configuration
└── requirements.txt          📦 Dependencies

📂 Documentation
├── PROJECT_STRUCTURE.md      📁 Complete file guide
├── SETUP_GUIDE.md           🚀 Setup instructions
└── EVALUATION_START_HERE.md  📊 Evaluation guide

📂 Agents (Core System)
├── agent_decision.py        🧠 Main routing
├── rag_agent/              📚 RAG components
├── image_analysis_agent/   🔬 Image analysis
└── web_search_processor/   🔍 Web search

📂 Data (Not in Git)
├── data/raw/              📄 Your PDFs
├── uploads/               📤 User uploads
└── evaluation_results/    📊 Test outputs
```

**👉 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed guide**

---

## 🚀 Usage

### 1. Agentic RAG (Main System)

```bash
python demo_agentic_rag.py
```

**What it does**:
- Processes medical queries through 4-agent workflow
- Retrieves relevant information from your knowledge base
- Generates accurate, source-attributed responses
- Self-corrects if retrieval quality is low

**Example**:
```python
from demo_agentic_rag import AgenticRAGSystem

rag = AgenticRAGSystem(
    pinecone_api_key="your_key",
    pinecone_index_name="medagentica",
    openrouter_api_key="your_groq_key"
)

response = rag.query("What are symptoms of diabetes?")
print(response['response'])
```

### 2. Web Application (Neo-Aurora Interface)

**Option A: Python Launcher (Recommended)**
```bash
python launch.py
```

**Option B: Manual Launch**
```bash
uvicorn app:app --reload
```

**Access**: http://localhost:8000

**Features**:
- 🌌 Beautiful Aurora-themed chat interface
- 📊 Live KPI dashboard with real-time metrics
- 🎨 Color-coded agent badges (Conversation, RAG, Web Search, Medical)
- 📎 Image upload with drag & drop support
- 💬 Markdown rendering with syntax highlighting
- 🖼️ Full-screen image modal viewer
- ⌨️ Keyboard shortcuts and accessibility features

### 2b. Agentic RAG Demo Web UI (NEW!)

**Modern ChatGPT-style interface for Agentic RAG system**

```bash
python demo_agentic_rag_web.py
```

**Access**: http://localhost:8001

**Features**:
- 💬 Clean, modern chat interface
- 📂 Conversation history in sidebar
- 📋 Copy, regenerate, and view metadata
- ℹ️ See query analysis, confidence scores, and sources
- 🎨 Professional design with smooth animations
- 📱 Responsive (works on mobile & desktop)

👉 See [DEMO_WEB_UI_GUIDE.md](DEMO_WEB_UI_GUIDE.md) for complete guide

### 3. Data Ingestion

```bash
python demo_ingest_pinecone.py
```

**What it does**:
- Loads PDFs from `./data/raw/`
- Extracts text & tables
- Chunks intelligently
- Uploads to Pinecone

### 4. Evaluation

**Quick (3 minutes)**:
```bash
python quick_evaluate.py
```

**Comprehensive (10 minutes)**:
```bash
python evaluate_rag_llm.py
```

**View Results**:
```bash
open evaluation_results/evaluation_report_*.html
```

---

## 🔑 Configuration

### Required API Keys:

1. **Pinecone** (Vector Database)
   - Get from: https://app.pinecone.io/
   - Free tier: 1 index, 100k vectors

2. **Groq** (Fast LLM - Recommended)
   - Get from: https://console.groq.com/
   - Free tier: Unlimited with rate limits
   - Model: `llama-3.3-70b-versatile`

**OR**

2. **OpenRouter** (Multiple Models)
   - Get from: https://openrouter.ai/
   - Pay-per-use pricing
   - Model: `deepseek/deepseek-chat-v3.1:free`

### Setup `.env`:

```bash
# Copy template
cp .env.example .env

# Edit with your keys
nano .env
```

```bash
# Required
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=medagentica-demo-384
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional
TAVILY_API_KEY=your_key  # Web search
ELEVEN_LABS_API_KEY=your_key  # Text-to-speech
```

---

## 📊 Evaluation Metrics Explained

### Accuracy Metrics
- **BLEU** (0-1): Word/phrase overlap with reference
  - Good: > 0.5
- **Semantic Similarity** (0-1): Meaning match using embeddings
  - Good: > 0.7

### RAG Quality
- **Faithfulness** (0-1): Answer grounded in documents?
  - Good: > 0.7
- **Hallucination** (0-1, **lower is better**): Making things up?
  - Good: < 0.3
- **Context Relevance** (0-1): Retrieved right documents?
  - Good: > 0.6

### Performance
- **TTFT**: Time to First Token (target: < 200ms)
- **Total Latency**: End-to-end time (target: < 2000ms)
- **Throughput**: Tokens/sec (target: > 50)

**👉 See [EVALUATION_README.md](EVALUATION_README.md) for details**

---

## 🛠️ Architecture

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

**Key Features**:
- **Chain of Thought**: Step-by-step reasoning
- **Self-Reflection**: Quality assessment & re-retrieval
- **Source Attribution**: Cites relevant documents
- **Context Grounding**: Prevents hallucinations

---

## 🤖 Available Agents

### 💬 Conversation Agent
**When to use:** General health questions, greetings, casual chat

### 📚 RAG Agent
**When to use:** Specific medical knowledge questions with document retrieval from your knowledge base

### 🌐 Web Search Agent
**When to use:** Latest medical research, current health news, recent publications

### 🧠 Brain Tumor Agent
**When to use:** Analyzing brain MRI scans for tumor detection and segmentation

### 🫁 Chest X-ray Agent
**When to use:** Analyzing chest X-rays for COVID-19 and 18+ diseases (Atelectasis, Pneumonia, etc.)

### 🩺 Skin Lesion Agent
**When to use:** Analyzing skin conditions with benign/malignant classification

---

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Complete history of changes and improvements
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup and configuration instructions
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Complete file organization guide

---


## 🧪 Testing & Validation

### Pre-Deployment Checklist:

```bash
# 1. Verify setup
python check_evaluation_setup.py

# 2. Quick test
python quick_evaluate.py

# 3. Full evaluation
python evaluate_rag_llm.py

# 4. Check metrics in HTML report
open evaluation_results/evaluation_report_*.html
```

### Success Criteria:
- ✅ BLEU > 0.5
- ✅ Hallucination < 0.3
- ✅ Faithfulness > 0.7
- ✅ Latency < 2000ms
- ✅ Success Rate > 95%

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. **Don't commit `.env` file!**
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Troubleshooting

### Common Issues:

**1. Import Error: `langchain_pinecone`**
```bash
# Fixed! Uses langchain_community.vectorstores instead
```

**2. Pinecone 401 Unauthorized**
```bash
# Check .env file has correct API key with pcsk_ prefix
# See FIX_PINECONE_KEY.md for details
```

**3. NLTK punkt_tab not found**
```bash
python -c "import nltk; nltk.download('punkt_tab')"
```

**4. Missing API Key**
```bash
# Copy template and add keys
cp .env.example .env
nano .env
```

**👉 See [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md) for more solutions**

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: Open GitHub issue
- **Questions**: Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🎉 Credits

Built with:
- 🦙 **LangChain** - RAG framework
- 📌 **Pinecone** - Vector database
- ⚡ **Groq** - Fast LLM inference
- 🤗 **HuggingFace** - Embeddings
- 🎨 **FastAPI** - Web framework

---

## 🚀 Quick Commands

```bash
# Main system
python demo_agentic_rag.py

# Web app
uvicorn app:app --reload

# Ingest data
python demo_ingest_pinecone.py

# Quick test
python quick_evaluate.py

# Full evaluation
python evaluate_rag_llm.py

# View results
open evaluation_results/evaluation_report_*.html
```

---

**⭐ Star this repo if you find it useful!**

**🔗 [Documentation](PROJECT_STRUCTURE.md) | [Setup Guide](SETUP_GUIDE.md) | [Evaluation](README_EVALUATION.md)**

