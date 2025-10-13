# 🔬 Complete RAG & LLM Evaluation System

## 📋 Table of Contents

1. [What This System Does](#what-this-system-does)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Files Overview](#files-overview)
4. [Understanding Metrics](#understanding-metrics)
5. [Step-by-Step Tutorial](#step-by-step-tutorial)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## What This System Does

This evaluation framework provides **comprehensive testing** for your RAG (Retrieval-Augmented Generation) and LLM systems. It measures:

### 🎯 **Accuracy Metrics** (Is it correct?)
- BLEU Score: Word/phrase similarity
- ROUGE Score: Content coverage
- Semantic Similarity: Meaning match

### 🔍 **RAG Quality** (Is it trustworthy?)
- Faithfulness: Grounded in documents?
- Answer Relevancy: Addresses the question?
- Context Relevance: Found right documents?
- Hallucination Detection: Making things up?

### ⚡ **Performance Metrics** (Is it fast & efficient?)
- Latency (TTFT, total time)
- Throughput (tokens/second)
- Memory usage

### 📊 **Outputs**
- Real-time console metrics
- Interactive HTML reports
- Beautiful visualizations
- JSON data for analysis

---

## Quick Start (5 Minutes)

### Step 1: Check Your Setup (1 min)

```bash
python check_evaluation_setup.py
```

This checks:
- ✅ Environment variables set
- ✅ Required packages installed
- ✅ Pinecone connection working
- ✅ Data ingested

**Fix any issues it reports before proceeding!**

### Step 2: Run Quick Evaluation (3 min)

```bash
python quick_evaluate.py
```

This will:
- Test 3 medical queries
- Show metrics in real-time
- Generate visualizations
- Create HTML report

### Step 3: View Results (1 min)

1. **Console**: Check metrics immediately
2. **HTML Report**: Open `./evaluation_results/evaluation_report_*.html` in browser
3. **Visualizations**: See `./evaluation_results/evaluation_visualizations_*.png`

**Done! You now know your system's performance.**

---

## Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| **check_evaluation_setup.py** | Verify environment is ready | Before any evaluation |
| **quick_evaluate.py** | Fast 3-query test | Quick health checks |
| **evaluate_rag_llm.py** | Comprehensive evaluation | Full testing before deployment |
| **EVALUATION_README.md** | Technical documentation | Understanding metrics in detail |
| **EVALUATION_USAGE_GUIDE.md** | Quick reference guide | Common tasks & fixes |
| **EVALUATION_COMPLETE_GUIDE.md** | This file - complete overview | Learning the system |

### Workflow

```
1. check_evaluation_setup.py  →  Verify setup
2. quick_evaluate.py           →  Quick test (3 queries)
3. evaluate_rag_llm.py         →  Full test (8+ queries)
4. Review HTML report          →  Analyze results
5. Apply optimizations         →  Fix issues
6. Re-run evaluation           →  Verify improvements
```

---

## Understanding Metrics

### 📊 Accuracy Metrics

#### BLEU Score (0-1 scale)
- **What**: Word/phrase overlap with reference
- **Good**: > 0.5 | **Fair**: 0.3-0.5 | **Poor**: < 0.3
- **Example**: 
  - Reference: "Diabetes symptoms include thirst and fatigue"
  - Generated: "Symptoms of diabetes are thirst and tiredness"
  - BLEU: ~0.6 (good overlap despite different words)

#### ROUGE Score (0-1 scale)
- **What**: How much reference content is captured
- **Good**: > 0.5 | **Fair**: 0.3-0.5 | **Poor**: < 0.3
- **Focus**: Recall (did we include important info?)

#### Semantic Similarity (0-1 scale)
- **What**: AI-based meaning comparison
- **Good**: > 0.7 | **Fair**: 0.5-0.7 | **Poor**: < 0.5
- **Advantage**: Understands paraphrasing

### 🔍 RAG Quality Metrics

#### Faithfulness (0-1 scale)
- **What**: Is answer grounded in retrieved documents?
- **Good**: > 0.7 | **Warning**: 0.5-0.7 | **Bad**: < 0.5
- **Critical**: Prevents hallucinations

#### Answer Relevancy (0-1 scale)
- **What**: Does answer address the question?
- **Good**: > 0.7 | **Fair**: 0.5-0.7 | **Poor**: < 0.5
- **Prevents**: Off-topic responses

#### Context Relevance (0-1 scale)
- **What**: Did retrieval find right documents?
- **Good**: > 0.6 | **Fair**: 0.4-0.6 | **Poor**: < 0.4
- **Indicates**: Vector search quality

#### Hallucination Score (0-1 scale, LOWER IS BETTER!)
- **What**: Is LLM inventing information?
- **Good**: < 0.2 | **Warning**: 0.2-0.4 | **Bad**: > 0.4
- **Formula**: 1 - (avg sentence support)

### ⚡ Performance Metrics

#### Latency
- **TTFT**: Time to First Token (target: < 200ms)
- **Total**: End-to-end time (target: < 2000ms)
- **Breakdown**: Retrieval + Generation time

#### Throughput
- **What**: Tokens processed per second
- **Good**: > 50 tok/s | **Fair**: 20-50 | **Slow**: < 20

---

## Step-by-Step Tutorial

### Tutorial 1: First Evaluation

```bash
# Step 1: Verify setup
python check_evaluation_setup.py

# Step 2: Run quick test
python quick_evaluate.py

# Step 3: Check console output
# Look for these key metrics:
#   - Success Rate (should be 100%)
#   - Avg BLEU (target: > 0.5)
#   - Avg Hallucination (target: < 0.3)
#   - Avg Latency (target: < 2000ms)

# Step 4: Open HTML report
open ./evaluation_results/evaluation_report_*.html
```

### Tutorial 2: Comprehensive Evaluation

```bash
# Run full test suite (8 queries)
python evaluate_rag_llm.py

# This will:
# 1. Test 8 different medical scenarios
# 2. Generate detailed statistics
# 3. Create visualizations
# 4. Produce comprehensive HTML report

# Review results:
# - Accuracy metrics (mean ± std)
# - RAG quality scores
# - Latency distribution
# - Performance trends
```

### Tutorial 3: Custom Test Cases

Create `my_medical_tests.py`:

```python
from evaluate_rag_llm import RAGLLMEvaluator
from demo_agentic_rag import AgenticRAGSystem
import os

# Initialize system
rag_system = AgenticRAGSystem(
    pinecone_api_key=os.getenv('PINECONE_API_KEY'),
    pinecone_index_name=os.getenv('PINECONE_INDEX_NAME'),
    openrouter_api_key=os.getenv('OPENROUTER_API_KEY')
)

evaluator = RAGLLMEvaluator(rag_system)

# Define your medical domain tests
custom_tests = [
    {
        'query': 'What are the side effects of metformin?',
        'reference_answer': '''Common side effects include nausea, diarrhea, 
        stomach upset, and metallic taste. Rare but serious side effect is 
        lactic acidosis.'''
    },
    {
        'query': 'When should I check blood glucose levels?',
        'reference_answer': '''Check fasting glucose in the morning, 
        before meals, 2 hours after meals, and before bedtime as recommended 
        by your doctor.'''
    },
    # Add more domain-specific tests
]

# Run evaluation
results = evaluator.evaluate_dataset(custom_tests)

# Print key metrics
print(f"BLEU: {results['accuracy_metrics']['bleu_score']['mean']:.3f}")
print(f"Faithfulness: {results['rag_metrics']['faithfulness']['mean']:.3f}")
print(f"Hallucination: {results['rag_metrics']['hallucination_score']['mean']:.3f}")
```

Run: `python my_medical_tests.py`

---

## Troubleshooting

### Problem 1: Setup Check Fails

**Error**: `PINECONE_API_KEY not set`

**Solution**:
```bash
# Create .env file
echo "PINECONE_API_KEY=your_key_here" >> .env
echo "PINECONE_INDEX_NAME=medagentica" >> .env
echo "OPENROUTER_API_KEY=your_key_here" >> .env
echo "OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1:free" >> .env

# Or export in terminal
export PINECONE_API_KEY='your_key_here'
```

### Problem 2: Index Has No Vectors

**Error**: `Index is empty`

**Solution**:
```bash
# Ingest your documents first
python demo_ingest_pinecone.py

# Verify ingestion
python check_evaluation_setup.py
```

### Problem 3: Missing Packages

**Error**: `No module named 'rouge_score'`

**Solution**:
```bash
# Install missing packages
pip install rouge-score pdfplumber

# Or install all requirements
pip install -r requirements.txt
```

### Problem 4: High Hallucination Score

**Symptom**: Hallucination > 0.4

**Solutions**:

1. **Strengthen prompts** in `demo_agentic_rag.py`:
```python
prompt = f"""IMPORTANT: Answer ONLY based on the context below. 
If unsure, say "I don't have enough information."

Context: {context}
Question: {query}"""
```

2. **Improve retrieval** (see below)

### Problem 5: Low Context Relevance

**Symptom**: Context Relevance < 0.5

**Solutions**:

1. **Adjust chunk size** in `demo_ingest_pinecone.py`:
```python
# Try different sizes: 512, 1000, 1500
chunk_size = 1000  # Increase for more context
chunk_overlap = 200
```

2. **Increase retrieval count** in `demo_agentic_rag.py`:
```python
# Retrieve more documents
k = 10  # Increase from 5 to 10
```

3. **Better embeddings**:
```python
# Use more powerful model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

### Problem 6: High Latency

**Symptom**: Latency > 3000ms

**Solutions**:

1. **Enable caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_retrieval(query):
    return vectorstore.similarity_search(query)
```

2. **Use faster model**:
```python
# In config
OPENROUTER_MODEL = "google/gemini-flash-1.5"  # Faster
```

3. **Optimize embedding**:
```python
# Use smaller, faster model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Fastest
)
```

---

## Advanced Usage

### Integration with CI/CD

Add to GitHub Actions (`.github/workflows/evaluate.yml`):

```yaml
name: RAG Evaluation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run evaluation
      env:
        PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
        OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
      run: |
        python evaluate_rag_llm.py
    
    - name: Upload results
      uses: actions/upload-artifact@v2
      with:
        name: evaluation-results
        path: ./evaluation_results/
```

### Monitoring Over Time

Track metrics across versions:

```python
import json
from datetime import datetime

# After evaluation
with open(f'./metrics_history/{datetime.now().isoformat()}.json', 'w') as f:
    json.dump(results, f)

# Analyze trends
import pandas as pd
import glob

files = glob.glob('./metrics_history/*.json')
metrics = []

for file in files:
    with open(file) as f:
        data = json.load(f)
        metrics.append({
            'timestamp': file,
            'bleu': data['accuracy_metrics']['bleu_score']['mean'],
            'hallucination': data['rag_metrics']['hallucination_score']['mean']
        })

df = pd.DataFrame(metrics)
print(df.describe())
```

### A/B Testing Different Prompts

```python
prompts = {
    'baseline': "Answer the question based on context: {context}\nQ: {query}\nA:",
    'strict': "ONLY use the context. If unsure, say so.\nContext: {context}\nQ: {query}\nA:",
    'cot': "Think step-by-step using context.\nContext: {context}\nQ: {query}\nThinking:"
}

for name, prompt_template in prompts.items():
    # Update prompt in system
    # Run evaluation
    results = evaluator.evaluate_dataset(test_cases)
    
    print(f"\n{name} Prompt:")
    print(f"  BLEU: {results['accuracy_metrics']['bleu_score']['mean']:.3f}")
    print(f"  Hallucination: {results['rag_metrics']['hallucination_score']['mean']:.3f}")
```

---

## Metrics Summary Cheat Sheet

| Metric | Range | Good | Warning | Action Needed |
|--------|-------|------|---------|---------------|
| **BLEU** | 0-1 | >0.5 | 0.3-0.5 | <0.3 - Improve prompts |
| **Semantic Sim** | 0-1 | >0.7 | 0.5-0.7 | <0.5 - Fine-tune model |
| **Faithfulness** | 0-1 | >0.7 | 0.5-0.7 | <0.5 - Better retrieval |
| **Hallucination** | 0-1 ⬇️ | <0.2 | 0.2-0.4 | >0.4 - Strengthen prompts |
| **Context Rel** | 0-1 | >0.6 | 0.4-0.6 | <0.4 - Tune chunks/embeddings |
| **TTFT** | ms | <200 | 200-500 | >500 - Optimize search |
| **Total Latency** | ms | <2000 | 2000-5000 | >5000 - Cache/optimize |
| **Throughput** | tok/s | >50 | 20-50 | <20 - Use GPU/quantize |

---

## Final Checklist

Before deploying to production:

- [ ] `python check_evaluation_setup.py` passes ✅
- [ ] `python quick_evaluate.py` shows good metrics ✅
- [ ] `python evaluate_rag_llm.py` comprehensive test passes ✅
- [ ] BLEU score > 0.5 ✅
- [ ] Hallucination < 0.3 ✅
- [ ] Faithfulness > 0.7 ✅
- [ ] Latency < 2000ms ✅
- [ ] Success rate > 95% ✅
- [ ] HTML report reviewed ✅
- [ ] Edge cases tested ✅
- [ ] Human validation for critical medical queries ✅

---

## Resources

- **Setup Checker**: `python check_evaluation_setup.py`
- **Quick Test**: `python quick_evaluate.py`
- **Full Test**: `python evaluate_rag_llm.py`
- **Technical Docs**: `EVALUATION_README.md`
- **Quick Guide**: `EVALUATION_USAGE_GUIDE.md`
- **This Guide**: `EVALUATION_COMPLETE_GUIDE.md`

---

## Next Steps

1. ✅ **Verify setup**: Run `python check_evaluation_setup.py`
2. 🚀 **Quick test**: Run `python quick_evaluate.py`
3. 📊 **Review results**: Open HTML report in browser
4. 🔧 **Fix issues**: Follow recommendations
5. 🔄 **Re-test**: Verify improvements
6. 🎉 **Deploy**: With confidence!

---

**You're all set! Start evaluating your RAG system now!** 🚀

For questions or issues, check the troubleshooting section or review the detailed technical documentation in `EVALUATION_README.md`.


