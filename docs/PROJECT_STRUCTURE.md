# 📁 Project Structure Guide

## 🎯 Quick Navigation

**New to the project?** Start here:
1. Read [README.md](README.md) - Project overview
2. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup instructions
3. Copy `.env.example` to `.env` and add your API keys
4. Run `python demo_agentic_rag.py` - Main RAG system
5. Run `python quick_evaluate.py` - Evaluate performance

---

## 📂 Directory Structure

```
Multi-Agent-Medical-Assistant/
│
├── 🚀 MAIN ENTRY POINTS
│   ├── demo_agentic_rag.py          # ⭐ MAIN: Agentic RAG System
│   ├── app.py                       # FastAPI Web Application
│   └── interactive_demo.py          # Interactive CLI Demo
│
├── 📊 EVALUATION SYSTEM
│   ├── quick_evaluate.py            # ⚡ Quick 3-min evaluation
│   ├── evaluate_rag_llm.py          # 📈 Comprehensive evaluation
│   ├── check_evaluation_setup.py    # ✅ Setup verification
│   └── setup_evaluation.py          # 🔧 Interactive setup wizard
│
├── 🔧 SETUP & CONFIGURATION
│   ├── .env.example                 # ⚠️ Template (copy to .env)
│   ├── .env                         # 🔒 YOUR SECRETS (not in git)
│   ├── config.py                    # System configuration
│   ├── requirements.txt             # Python dependencies
│   └── setup_evaluation_env.sh      # Bash setup script
│
├── 📚 DOCUMENTATION
│   ├── README.md                    # ⭐ Start here!
│   ├── SETUP_GUIDE.md              # Setup instructions
│   ├── PROJECT_STRUCTURE.md         # This file
│   ├── ARCHITECTURE.txt             # System architecture
│   ├── DEMO_README.md              # Demo system docs
│   ├── DEMO_SUMMARY.md             # Demo summary
│   └── COMPARISON.md               # Feature comparison
│
├── 📊 EVALUATION DOCS
│   ├── README_EVALUATION.md         # Evaluation index
│   ├── EVALUATION_START_HERE.md     # Getting started
│   ├── EVALUATION_QUICKREF.md       # Quick reference
│   ├── EVALUATION_USAGE_GUIDE.md    # Usage guide
│   ├── EVALUATION_COMPLETE_GUIDE.md # Complete tutorial
│   ├── EVALUATION_README.md         # Technical docs
│   ├── EVALUATION_SUMMARY.md        # Summary
│   ├── EVALUATION_VISUAL_GUIDE.md   # Visual flowcharts
│   ├── EVALUATION_WHAT_WAS_CREATED.md # Inventory
│   ├── QUICK_FIX_GUIDE.md          # Troubleshooting
│   └── FIX_PINECONE_KEY.md         # Pinecone fixes
│
├── 🧠 AGENTS (Core System)
│   ├── agent_decision.py            # Main routing agent
│   │
│   ├── rag_agent/                   # RAG System
│   │   ├── vectorstore_chroma.py   # ChromaDB integration
│   │   ├── vectorstore_qdrant.py   # Qdrant integration
│   │   ├── content_processor.py    # Content processing
│   │   ├── doc_parser.py           # Document parsing
│   │   ├── query_expander.py       # Query expansion
│   │   ├── reranker.py             # Result reranking
│   │   └── response_generator.py   # Response generation
│   │
│   ├── image_analysis_agent/       # Medical Image Analysis
│   │   ├── image_classifier.py     # Main classifier
│   │   ├── brain_tumor_agent/      # Brain tumor detection
│   │   ├── chest_xray_agent/       # Chest X-ray analysis
│   │   └── skin_lesion_agent/      # Skin lesion detection
│   │
│   ├── web_search_processor_agent/ # Web Search
│   │   ├── web_search_agent.py     # Main search agent
│   │   ├── web_search_processor.py # Search processing
│   │   ├── pubmed_search.py        # PubMed integration
│   │   └── tavily_search.py        # Tavily integration
│   │
│   └── guardrails/                  # Safety & Validation
│       └── local_guardrails.py     # Content moderation
│
├── 🗄️ DATA INGESTION
│   ├── demo_ingest_pinecone.py     # ⭐ Ingest to Pinecone
│   └── ingest_rag_data.py          # General ingestion
│
├── 🧪 TESTING
│   ├── test_full_config.py         # Full system test
│   └── test_openrouter_config.py   # OpenRouter test
│
├── 🌐 WEB INTERFACE
│   └── templates/
│       └── index.html              # Web UI
│
├── 🎨 ASSETS
│   └── assets/
│       ├── logo.jpg               # Project logo
│       ├── *.png                  # Flowcharts
│       └── *.mp4                  # Demo videos
│
├── 📦 DATA (Not in Git)
│   ├── raw/                       # PDF documents
│   ├── chroma_db/                # ChromaDB storage
│   ├── qdrant_db/                # Qdrant storage
│   ├── docs_db/                  # Document database
│   └── parsed_docs/              # Parsed content
│
├── 📤 UPLOADS (Not in Git)
│   ├── backend/                  # Backend uploads
│   ├── frontend/                 # Frontend uploads
│   ├── speech/                   # Audio files
│   └── skin_lesion_output/       # Analysis results
│
├── 📊 OUTPUTS (Not in Git)
│   └── evaluation_results/       # Evaluation outputs
│       ├── *.json               # Raw metrics
│       ├── *.png                # Visualizations
│       └── *.html               # Reports
│
└── 🔒 SENSITIVE (Never Commit!)
    ├── .env                      # Your API keys
    ├── venv/                     # Virtual environment
    └── __pycache__/             # Python cache
```

---

## 🚀 Main Files Explained

### 1. **demo_agentic_rag.py** ⭐ MAIN SYSTEM
**Purpose**: Primary agentic RAG system with multi-agent workflow

**What it does**:
- Query Analysis Agent: Analyzes user questions
- Retrieval Agent: Fetches relevant documents from Pinecone
- Reflection Agent: Evaluates retrieval quality
- Response Synthesis Agent: Generates final answers

**When to use**: 
- Production RAG queries
- Testing RAG functionality
- Demo purposes

**How to run**:
```bash
python demo_agentic_rag.py
```

---

### 2. **app.py** - Web Application
**Purpose**: FastAPI web server with REST API

**Features**:
- `/chat` - Text chat endpoint
- `/upload` - Image upload & analysis
- `/validate` - Human validation
- `/transcribe` - Speech-to-text
- `/generate-speech` - Text-to-speech

**How to run**:
```bash
uvicorn app:app --reload
```

---

### 3. **demo_ingest_pinecone.py** - Data Ingestion
**Purpose**: Ingest PDF documents into Pinecone

**What it does**:
- Extracts text from PDFs
- Chunks documents intelligently
- Generates embeddings
- Uploads to Pinecone

**When to use**: First time setup or adding new documents

**How to run**:
```bash
python demo_ingest_pinecone.py
```

---

### 4. **quick_evaluate.py** - Quick Testing
**Purpose**: 3-minute evaluation of RAG system

**Metrics**:
- Accuracy (BLEU, ROUGE, Semantic)
- RAG Quality (Faithfulness, Hallucination)
- Performance (Latency, Throughput)

**How to run**:
```bash
python quick_evaluate.py
```

---

### 5. **evaluate_rag_llm.py** - Comprehensive Evaluation
**Purpose**: Full evaluation with 15+ metrics

**Outputs**:
- JSON data files
- Visualization charts (PNG)
- Interactive HTML reports

**How to run**:
```bash
python evaluate_rag_llm.py
```

---

## 🔑 Environment Variables

### Required (Must Set):
```bash
PINECONE_API_KEY=pcsk_xxxxx    # Pinecone vector DB
GROQ_API_KEY=gsk_xxxxx          # Groq LLM (or OpenRouter)
```

### Optional:
```bash
TAVILY_API_KEY=xxxxx           # Web search
ELEVEN_LABS_API_KEY=xxxxx      # Text-to-speech
```

**Setup**:
1. Copy `.env.example` to `.env`
2. Fill in your actual API keys
3. Never commit `.env` to git!

---

## 📚 Documentation Map

### For Beginners:
1. [README.md](README.md) - Overview
2. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup
3. [EVALUATION_START_HERE.md](EVALUATION_START_HERE.md) - Evaluation basics

### For Users:
1. [DEMO_README.md](DEMO_README.md) - How to use
2. [EVALUATION_USAGE_GUIDE.md](EVALUATION_USAGE_GUIDE.md) - Evaluation guide
3. [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md) - Troubleshooting

### For Developers:
1. [ARCHITECTURE.txt](ARCHITECTURE.txt) - System design
2. [EVALUATION_README.md](EVALUATION_README.md) - Technical evaluation
3. [config.py](config.py) - Configuration

---

## 🔒 Security & Git

### Files in `.gitignore` (Never Commit):
- `.env` - Your secrets!
- `data/` - Large datasets
- `uploads/` - User uploads
- `evaluation_results/` - Generated outputs
- `venv/` - Python environment
- `*.pth` - Model weights
- `__pycache__/` - Python cache

### Safe to Commit:
- `.env.example` - Template (no secrets)
- `*.py` - All code files
- `*.md` - Documentation
- `requirements.txt` - Dependencies
- `.gitignore` - Git configuration

---

## 🎯 Common Workflows

### First Time Setup:
```bash
# 1. Clone & install
git clone <repo>
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Ingest data
python demo_ingest_pinecone.py

# 4. Test
python demo_agentic_rag.py
```

### Daily Development:
```bash
# 1. Quick test
python quick_evaluate.py

# 2. Make changes to demo_agentic_rag.py

# 3. Re-test
python quick_evaluate.py

# 4. Full evaluation before commit
python evaluate_rag_llm.py
```

### Deployment:
```bash
# 1. Full evaluation
python evaluate_rag_llm.py

# 2. Check metrics in HTML report
open evaluation_results/evaluation_report_*.html

# 3. Start web server
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 📊 Evaluation Results

Located in `evaluation_results/` (not in git):

**Files**:
- `evaluation_results_TIMESTAMP.json` - Raw metrics
- `evaluation_visualizations_TIMESTAMP.png` - Charts
- `evaluation_report_TIMESTAMP.html` - Interactive report

**View**:
```bash
open evaluation_results/evaluation_report_*.html
```

---

## 🆘 Quick Help

**Where is...**
- Main RAG system? → `demo_agentic_rag.py`
- Web server? → `app.py`
- Evaluation? → `quick_evaluate.py`
- Setup guide? → `SETUP_GUIDE.md`
- Secrets template? → `.env.example`

**How do I...**
- Add API keys? → Copy `.env.example` to `.env`
- Ingest documents? → Run `python demo_ingest_pinecone.py`
- Test RAG? → Run `python demo_agentic_rag.py`
- Evaluate? → Run `python quick_evaluate.py`
- Deploy? → Run `uvicorn app:app`

---

**Need more help?** See [README.md](README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)

