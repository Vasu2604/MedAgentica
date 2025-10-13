# ⚡ RAG Evaluation - Quick Reference Card

## 🚀 Commands (Copy & Paste)

### Setup & Verification
```bash
# Check if ready to evaluate
python check_evaluation_setup.py

# Install missing packages
pip install rouge-score pdfplumber

# Set environment (replace with your keys)
export PINECONE_API_KEY='your_key_here'
export OPENROUTER_API_KEY='your_key_here'
```

### Run Evaluations
```bash
# Quick test (3 queries, ~3 min)
python quick_evaluate.py

# Full test (8 queries, ~10 min)
python evaluate_rag_llm.py

# View results
open ./evaluation_results/evaluation_report_*.html
```

---

## 📊 Metrics Cheat Sheet

| Metric | Good | Warning | Bad | Fix |
|--------|------|---------|-----|-----|
| **BLEU** | >0.5 | 0.3-0.5 | <0.3 | Better prompts |
| **Faithfulness** | >0.7 | 0.5-0.7 | <0.5 | Improve retrieval |
| **Hallucination** ⬇️ | <0.2 | 0.2-0.4 | >0.4 | Strengthen grounding |
| **Context Rel** | >0.6 | 0.4-0.6 | <0.4 | Tune chunks |
| **Latency** | <2s | 2-5s | >5s | Cache/optimize |

---

## 🔧 Quick Fixes

### High Hallucination (>0.3)
```python
# Strengthen prompt
prompt = "Answer ONLY from context. If unsure, say so.\n{context}\n{query}"
```

### Slow Response (>3s)
```python
# Enable caching
from functools import lru_cache
@lru_cache(maxsize=100)
def get_answer(query): ...
```

### Poor Retrieval (<0.5)
```python
# Increase documents
k = 10  # Change from 5 to 10

# Better chunks
chunk_size = 1000  # Increase size
```

---

## 📁 Files Guide

| File | Use When |
|------|----------|
| `check_evaluation_setup.py` | First time / debugging |
| `quick_evaluate.py` | Daily checks |
| `evaluate_rag_llm.py` | Before deployment |
| `EVALUATION_COMPLETE_GUIDE.md` | Learning |
| `EVALUATION_QUICKREF.md` | This file! |

---

## ✅ Pre-Deployment Checklist

- [ ] `check_evaluation_setup.py` ✅
- [ ] BLEU > 0.5 ✅
- [ ] Hallucination < 0.3 ✅
- [ ] Latency < 2000ms ✅
- [ ] HTML report reviewed ✅
- [ ] Human validation ✅

---

## 🆘 Common Errors

| Error | Solution |
|-------|----------|
| "API key not found" | `export PINECONE_API_KEY='key'` |
| "Index empty" | `python demo_ingest_pinecone.py` |
| "Module not found" | `pip install rouge-score` |
| Slow evaluation | Use fewer test cases |

---

## 📊 Understanding Output

### Console Output
```
✅ Success Rate: 100%        ← All working
📊 Avg BLEU: 0.682          ← Good accuracy
📚 Avg Hallucination: 0.208  ← Low risk ✅
⏱️  Avg Latency: 1834ms      ← Fast ✅
```

### What This Means
- ✅ System ready for production
- ✅ Answers are accurate
- ✅ Low hallucination risk
- ✅ Fast response time

---

## 🎯 Optimization Priority

1. **Hallucination > 0.4** → Fix FIRST (safety)
2. **BLEU < 0.3** → Fix accuracy
3. **Latency > 5s** → Optimize speed
4. **Context < 0.5** → Improve retrieval

---

## 💡 Quick Tips

- Run `quick_evaluate.py` daily for health checks
- Review HTML reports for detailed insights
- Track metrics over time in JSON files
- Test with domain-specific queries
- Get human validation for critical medical answers

---

**Keep this card handy for quick reference!** 📌

Full docs: `EVALUATION_COMPLETE_GUIDE.md`


