# 🚀 Quick Start: Evaluation in 5 Minutes

## Step 1: Install Dependencies (30 seconds)

```bash
pip install rouge-score pdfplumber
```

## Step 2: Set Environment Variables (1 minute)

Create a `.env` file or export in terminal:

```bash
export PINECONE_API_KEY='your_pinecone_api_key_here'
export PINECONE_INDEX_NAME='medagentica'
export OPENROUTER_API_KEY='your_openrouter_api_key_here'
export OPENROUTER_MODEL='deepseek/deepseek-chat-v3.1:free'
```

## Step 3: Run Quick Evaluation (3 minutes)

```bash
python quick_evaluate.py
```

This will:
- Test 3 medical queries
- Show real-time metrics
- Generate visualizations
- Create HTML report

## Step 4: View Results

1. **Console Output**: See metrics immediately
2. **Visualizations**: `./evaluation_results/evaluation_visualizations_*.png`
3. **HTML Report**: `./evaluation_results/evaluation_report_*.html` (open in browser)
4. **JSON Data**: `./evaluation_results/evaluation_results_*.json`

---

## 📊 Understanding Your Results

### What the Metrics Mean (Simple English):

#### ✅ **BLEU Score** (0-1)
- **What it is**: How similar your answer is to the expected answer (word-by-word)
- **Good score**: > 0.5
- **Bad score**: < 0.3
- **Fix if low**: Improve prompts, use better model

#### ✅ **Semantic Similarity** (0-1)
- **What it is**: Do answers have the same MEANING (even with different words)?
- **Good score**: > 0.7
- **Bad score**: < 0.5
- **Fix if low**: Better prompts, domain fine-tuning

#### ✅ **Faithfulness** (0-1)
- **What it is**: Is the answer supported by your documents?
- **Good score**: > 0.7
- **Bad score**: < 0.5
- **Fix if low**: Improve retrieval, add grounding prompts

#### ✅ **Hallucination Score** (0-1, LOWER is better!)
- **What it is**: Is the AI making things up?
- **Good score**: < 0.3
- **Bad score**: > 0.5
- **Fix if high**: Strengthen prompts ("answer only from context"), better retrieval

#### ✅ **Context Relevance** (0-1)
- **What it is**: Is your search finding the right documents?
- **Good score**: > 0.6
- **Bad score**: < 0.4
- **Fix if low**: Adjust chunk size, better embeddings, increase retrieval count

#### ✅ **Latency** (milliseconds)
- **What it is**: How fast your system responds
- **Good**: < 2000ms (2 seconds)
- **Bad**: > 5000ms (5 seconds)
- **Fix if high**: Cache results, faster models, optimize search

#### ✅ **Throughput** (tokens/second)
- **What it is**: How many words processed per second
- **Good**: > 50 tokens/sec
- **Bad**: < 20 tokens/sec
- **Fix if low**: Use GPU, batch processing, quantization

---

## 🎯 Quick Decision Guide

### Is Your System Good?

Run `python quick_evaluate.py` and check:

1. **✅ All metrics GREEN?** → System is production-ready!
2. **⚠️ Some metrics YELLOW?** → Works but needs tuning
3. **❌ Many metrics RED?** → Needs significant improvement

### Common Issues & Solutions

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **Making things up** | High hallucination (>0.4) | Add "answer only from context" to prompts |
| **Wrong answers** | Low BLEU (<0.3) | Better prompts or fine-tune model |
| **Slow responses** | High latency (>3000ms) | Enable caching, use faster model |
| **Finding wrong docs** | Low context relevance (<0.5) | Adjust chunk size, better embeddings |

---

## 📝 Sample Output Explained

When you run the evaluation, you'll see:

```
📊 RESULTS SUMMARY:
   • Success Rate: 100.0%           ← All queries worked
   • Avg BLEU Score: 0.682           ← Pretty good accuracy
   • Avg Semantic Similarity: 0.834  ← Excellent meaning match!
   • Avg Faithfulness: 0.792         ← Well-grounded in documents
   • Avg Hallucination: 0.208        ← Low hallucination risk ✅
   • Avg Latency: 1834ms             ← Fast response (under 2 sec) ✅
   • Avg Throughput: 87.3 tok/s      ← Good processing speed
```

### What This Means:
- ✅ **System is working well** - answers are accurate and fast
- ✅ **Low hallucination** - trustworthy responses
- ✅ **Good latency** - responsive user experience
- 💡 **Could improve BLEU** - fine-tune for better word matching

---

## 🔧 Quick Fixes

### Fix 1: High Hallucination
**Problem**: Hallucination score > 0.3

**Solution**: Update your prompt in `demo_agentic_rag.py`:
```python
prompt = f"""You are a medical assistant. 
IMPORTANT: Answer ONLY based on the provided context below. 
If the context doesn't contain the answer, say "I don't have enough information."

Context: {context}
Question: {query}
Answer:"""
```

### Fix 2: Slow Response
**Problem**: Latency > 3000ms

**Solution**: Enable caching:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_text):
    return rag_system.query(query_text)
```

### Fix 3: Poor Retrieval
**Problem**: Context relevance < 0.5

**Solution**: Increase retrieval count in `demo_agentic_rag.py`:
```python
# Change from 5 to 10 documents
retrieved_docs = self.vectorstore.similarity_search(query, k=10)
```

---

## 📊 Advanced: Custom Test Cases

Create your own test file `my_tests.py`:

```python
from evaluate_rag_llm import RAGLLMEvaluator
from demo_agentic_rag import AgenticRAGSystem
import os

# Initialize
rag_system = AgenticRAGSystem(
    pinecone_api_key=os.getenv('PINECONE_API_KEY'),
    pinecone_index_name=os.getenv('PINECONE_INDEX_NAME'),
    openrouter_api_key=os.getenv('OPENROUTER_API_KEY')
)

evaluator = RAGLLMEvaluator(rag_system)

# Your custom tests
my_tests = [
    {
        'query': 'What causes high blood pressure?',
        'reference_answer': 'High blood pressure can be caused by genetics, obesity, high salt intake, stress, lack of exercise, and certain medical conditions.'
    },
    {
        'query': 'How to prevent heart disease?',
        'reference_answer': 'Prevention includes healthy diet, regular exercise, maintaining healthy weight, not smoking, limiting alcohol, and managing stress.'
    }
]

# Run evaluation
results = evaluator.evaluate_dataset(my_tests)

# Print summary
print(f"Average BLEU: {results['accuracy_metrics']['bleu_score']['mean']:.3f}")
print(f"Average Hallucination: {results['rag_metrics']['hallucination_score']['mean']:.3f}")
```

Run with: `python my_tests.py`

---

## 🎓 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `evaluate_rag_llm.py` | Full evaluation framework | Comprehensive testing |
| `quick_evaluate.py` | Fast 3-query test | Quick checks |
| `EVALUATION_README.md` | Detailed documentation | Learning about metrics |
| `EVALUATION_USAGE_GUIDE.md` | This guide | Getting started |

---

## ✅ Checklist: Is Your System Ready?

Before deploying to production:

- [ ] Run `python evaluate_rag_llm.py` on full test set
- [ ] BLEU score > 0.5
- [ ] Hallucination < 0.3
- [ ] Latency < 2000ms
- [ ] Success rate > 95%
- [ ] Review HTML report for issues
- [ ] Test with edge cases
- [ ] Get human validation for medical accuracy

---

## 🆘 Troubleshooting

### Error: "PINECONE_API_KEY not found"
```bash
export PINECONE_API_KEY='paste_your_key_here'
```

### Error: "No module named 'rouge_score'"
```bash
pip install rouge-score
```

### Error: "Index not found"
First run ingestion:
```bash
python demo_ingest_pinecone.py
```

### Slow evaluation
- Use fewer test cases: Edit `create_medical_test_dataset()` to return only 3 cases
- Use GPU: Ensure PyTorch uses CUDA
- Close other apps to free memory

---

## 📞 Getting Help

1. Check console error messages
2. Review `./evaluation_results/` files
3. Run with verbose mode: `verbose=True`
4. Check logs in terminal output

---

## 🎉 Success!

You now know how to:
- ✅ Run evaluations in minutes
- ✅ Understand all metrics
- ✅ Fix common issues
- ✅ Create custom tests
- ✅ Deploy with confidence

**Next**: Run `python quick_evaluate.py` and see your results!

---

*For detailed technical information, see `EVALUATION_README.md`*


