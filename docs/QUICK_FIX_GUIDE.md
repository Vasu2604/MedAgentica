# ⚡ Quick Fix Guide - Setup Issues

## ✅ Issue Fixed!

I've installed the missing `rouge-score` package and created setup tools for you.

---

## 🚀 Two Ways to Fix Environment Variables

### Option 1: Interactive Setup (Recommended)

Run this command and follow the prompts:

```bash
python setup_evaluation.py
```

This will:
- ✅ Install missing packages
- ✅ Prompt for API keys
- ✅ Create/update .env file
- ✅ Verify setup automatically

### Option 2: Manual Setup

1. **Create `.env` file** in the project root:

```bash
# In Multi-Agent-Medical-Assistant directory
nano .env
```

2. **Add these lines** (replace with your actual keys):

```bash
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=medagentica
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1:free
```

3. **Load environment variables**:

```bash
# Option A: For current terminal session
export $(cat .env | grep -v '^#' | xargs)

# Option B: For bash users, add to ~/.bashrc or ~/.bash_profile
source .env

# Option C: For zsh users, add to ~/.zshrc
source .env
```

---

## 📋 Where to Get API Keys

### Pinecone API Key
1. Go to https://www.pinecone.io/
2. Sign up/Login
3. Go to "API Keys" in dashboard
4. Copy your API key
5. Paste in `.env` file

### OpenRouter API Key
1. Go to https://openrouter.ai/
2. Sign up/Login
3. Go to "Keys" section
4. Create new key
5. Copy and paste in `.env` file

---

## ✅ Verify Setup

After setting up environment variables, run:

```bash
python check_evaluation_setup.py
```

You should see all ✅ green checkmarks!

---

## 🔄 If Pinecone Index is Empty

If the checker says "Index is empty", run:

```bash
python demo_ingest_pinecone.py
```

This will populate your Pinecone index with medical documents.

---

## 🎯 Quick Test

Once everything is set up:

```bash
python quick_evaluate.py
```

This runs a 3-minute evaluation and shows your results!

---

## 🆘 Still Having Issues?

### Check 1: Environment variables loaded?
```bash
echo $PINECONE_API_KEY
echo $OPENROUTER_API_KEY
```

If empty, reload:
```bash
export $(cat .env | grep -v '^#' | xargs)
```

### Check 2: Packages installed?
```bash
pip list | grep rouge-score
pip list | grep pdfplumber
```

If missing:
```bash
pip install rouge-score pdfplumber
```

### Check 3: In correct directory?
```bash
pwd
# Should show: .../MedAgentica/Multi-Agent-Medical-Assistant
```

If not:
```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
```

---

## 📝 Summary

**What I fixed:**
1. ✅ Installed `rouge-score` package
2. ✅ Created `setup_evaluation.py` (interactive setup)
3. ✅ Created `setup_evaluation_env.sh` (bash script)
4. ✅ Made scripts executable

**What you need to do:**
1. Set up API keys (run `python setup_evaluation.py`)
2. Verify setup (`python check_evaluation_setup.py`)
3. Ingest data if needed (`python demo_ingest_pinecone.py`)
4. Run evaluation (`python quick_evaluate.py`)

---

## 🎉 Next Steps

Once setup is complete:

1. **Run quick evaluation:**
   ```bash
   python quick_evaluate.py
   ```

2. **View results:**
   ```bash
   open ./evaluation_results/evaluation_report_*.html
   ```

3. **Read the guide:**
   ```bash
   cat EVALUATION_START_HERE.md
   ```

---

**You're almost there! Just set up your API keys and you're ready to go!** 🚀

