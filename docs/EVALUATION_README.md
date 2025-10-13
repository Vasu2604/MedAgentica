# 🔬 RAG & LLM Evaluation Framework

## Overview

This comprehensive evaluation framework helps you measure and optimize your RAG (Retrieval-Augmented Generation) and LLM system across multiple dimensions:

### 📊 **Evaluation Metrics**

#### 1. **Accuracy Metrics** (Trustworthiness)
- **BLEU Score**: Measures word/phrase overlap with reference answers (0-1 scale)
  - *What it means*: How similar the generated text is to the expected answer
  - *Good score*: > 0.5
  
- **ROUGE Scores**: Evaluates content coverage and recall
  - *What it means*: How much of the reference information is captured
  - *Good score*: ROUGE-L > 0.5
  
- **Semantic Similarity**: AI-based meaning comparison using embeddings
  - *What it means*: Do answers convey the same meaning even with different wording?
  - *Good score*: > 0.7

#### 2. **RAG Quality Metrics**
- **Faithfulness**: How grounded the answer is in retrieved context
  - *What it means*: Is the answer supported by your documents?
  - *Good score*: > 0.7
  
- **Answer Relevancy**: How well the answer addresses the question
  - *What it means*: Does the answer stay on-topic?
  - *Good score*: > 0.7
  
- **Context Relevance**: Quality of document retrieval
  - *What it means*: Is your vector search finding the right documents?
  - *Good score*: > 0.6
  
- **Hallucination Score**: Detection of unsupported claims
  - *What it means*: Is the LLM making things up? (LOWER is better)
  - *Good score*: < 0.3

#### 3. **Latency Metrics** (Responsiveness)
- **TTFT** (Time to First Token): Initial response delay
  - *Target*: < 200ms for real-time feel
  
- **Total Latency**: End-to-end response time
  - *Target*: < 2000ms for good UX
  
- **Retrieval Time**: Vector database search duration
  
- **Generation Time**: LLM inference time

#### 4. **Performance Metrics** (Scalability)
- **Throughput**: Tokens processed per second
  - *Target*: > 50 tokens/sec
  
- **Memory Usage**: RAM consumption
  
- **Success Rate**: Percentage of successful completions

---

## 🚀 Quick Start

### Prerequisites

1. **Install dependencies**:
```bash
pip install rouge-score pdfplumber
# Or install all requirements:
pip install -r requirements.txt
```

2. **Set up environment variables** (create `.env` file):
```bash
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=medagentica
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1:free
```

### Run Evaluation

#### Option 1: Use Pre-defined Test Dataset
```bash
python evaluate_rag_llm.py
```

This will:
- Run 8 medical test queries
- Generate comprehensive metrics
- Create visualizations
- Generate HTML report

#### Option 2: Custom Test Cases

Edit the `create_medical_test_dataset()` function in `evaluate_rag_llm.py`:

```python
def create_medical_test_dataset():
    return [
        {
            'query': 'Your medical question here',
            'reference_answer': 'Expected answer for comparison'
        },
        # Add more test cases...
    ]
```

#### Option 3: Evaluate Single Query

```python
from evaluate_rag_llm import RAGLLMEvaluator
from demo_agentic_rag import AgenticRAGSystem

# Initialize
rag_system = AgenticRAGSystem(
    pinecone_api_key="your_key",
    pinecone_index_name="medagentica",
    openrouter_api_key="your_key"
)

evaluator = RAGLLMEvaluator(rag_system)

# Evaluate single query
result = evaluator.evaluate_single_query(
    query="What are symptoms of diabetes?",
    reference_answer="Common symptoms include increased thirst, frequent urination...",
    verbose=True
)

print(f"BLEU Score: {result['accuracy']['bleu_score']}")
print(f"Latency: {result['latency']['total_latency_ms']}ms")
```

---

## 📂 Output Files

After running evaluation, you'll find in `./evaluation_results/`:

### 1. **JSON Results** (`evaluation_results_TIMESTAMP.json`)
- Complete raw data
- All metrics for each test case
- Aggregated statistics
- Use for programmatic access

### 2. **Visualizations** (`evaluation_visualizations_TIMESTAMP.png`)
- Accuracy metrics bar chart
- RAG quality metrics
- Latency distribution histogram
- Latency breakdown (retrieval vs generation)
- Throughput over time
- Memory usage tracking

### 3. **HTML Report** (`evaluation_report_TIMESTAMP.html`)
- Interactive, easy-to-read report
- Detailed explanations of each metric
- Color-coded performance indicators
- Actionable recommendations
- **Open in browser for best experience!**

---

## 📈 Understanding Your Results

### Accuracy Metrics Interpretation

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| BLEU Score | > 0.7 | 0.5-0.7 | 0.3-0.5 | < 0.3 |
| ROUGE-L | > 0.7 | 0.5-0.7 | 0.3-0.5 | < 0.3 |
| Semantic Similarity | > 0.8 | 0.6-0.8 | 0.4-0.6 | < 0.4 |

### RAG Quality Interpretation

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| Faithfulness | > 0.8 | 0.6-0.8 | 0.4-0.6 | < 0.4 |
| Answer Relevancy | > 0.8 | 0.6-0.8 | 0.4-0.6 | < 0.4 |
| Context Relevance | > 0.7 | 0.5-0.7 | 0.3-0.5 | < 0.3 |
| Hallucination | < 0.2 | 0.2-0.3 | 0.3-0.5 | > 0.5 |

### Latency Targets

| Metric | Target | Good | Acceptable | Slow |
|--------|--------|------|------------|------|
| TTFT | < 200ms | < 200ms | 200-500ms | > 500ms |
| Total Latency | < 2000ms | < 1500ms | 1500-3000ms | > 3000ms |
| Retrieval | < 500ms | < 300ms | 300-800ms | > 800ms |

---

## 🛠️ Optimization Tips

### If BLEU/Accuracy is Low:
1. **Fine-tune your LLM** on domain-specific medical data
2. **Improve prompt engineering** with better instructions
3. **Add few-shot examples** in prompts
4. **Use more powerful models** (e.g., GPT-4 instead of GPT-3.5)

### If Hallucination is High:
1. **Strengthen grounding prompts**: "Answer ONLY based on the provided context"
2. **Improve retrieval quality** (see below)
3. **Lower LLM temperature** (more deterministic)
4. **Add citation requirements** in prompts

### If Context Relevance is Low:
1. **Tune chunk size** (try 512, 1000, 1500 tokens)
2. **Adjust chunk overlap** (100-200 tokens)
3. **Improve embeddings**: Try different models (e.g., `sentence-transformers/all-mpnet-base-v2`)
4. **Increase retrieval count** (retrieve top-10 instead of top-5)
5. **Add query expansion** or reformulation

### If Latency is High:
1. **Use faster embeddings**: Switch to smaller models
2. **Enable caching**: Cache frequently asked queries
3. **Quantize LLM**: Use 8-bit or 4-bit quantization
4. **Optimize vector search**: Better indexing, approximate search
5. **Use streaming responses**: Show partial results early
6. **Batch processing**: Process multiple queries together

### If Throughput is Low:
1. **Use GPU acceleration**: Ensure CUDA is enabled
2. **Batch inference**: Process multiple queries at once
3. **Use vLLM or TensorRT**: Optimized inference engines
4. **Reduce context length**: Limit retrieved chunks

---

## 📊 Example Evaluation Output

### Console Output:
```
================================================================================
🔍 Evaluating Query: What are the common symptoms of type 2 diabetes?
================================================================================

📊 Calculating Accuracy Metrics...
📚 Calculating RAG Metrics...
⏱️  Measuring Latency...
💻 Measuring Performance...

✅ Evaluation Complete!

📈 ACCURACY METRICS:
   BLEU Score: 0.721 (0=poor, 1=perfect)
   ROUGE-L: 0.685 (recall coverage)
   Semantic Similarity: 0.834 (meaning match)

📚 RAG QUALITY METRICS:
   Faithfulness: 0.792 (context grounding)
   Answer Relevancy: 0.856 (addresses question)
   Context Relevance: 0.724 (retrieval quality)
   Hallucination Score: 0.208 (0=none, 1=high)

⏱️  LATENCY METRICS:
   TTFT: 145.2ms (target: <200ms)
   Total Latency: 1834.5ms (target: <2000ms)
   Retrieval Time: 423.1ms

💻 PERFORMANCE METRICS:
   Throughput: 87.3 tokens/sec
   Memory Usage: 1247.8 MB
   Total Tokens: 342
```

### HTML Report Preview:
- ✅ **Success Rate**: 100% (8/8 queries)
- 📊 **Average BLEU**: 0.682
- ⏱️ **Average Latency**: 1923ms
- 🚀 **Average Throughput**: 82.5 tok/s

---

## 🔧 Advanced Usage

### Custom Metrics

Add your own evaluation metrics by extending the `RAGLLMEvaluator` class:

```python
class CustomEvaluator(RAGLLMEvaluator):
    def calculate_custom_metric(self, answer: str, context: str) -> float:
        # Your custom metric logic
        return score
```

### Integration with CI/CD

```bash
# In your CI pipeline
python evaluate_rag_llm.py
if [ $? -eq 0 ]; then
    echo "Evaluation passed"
else
    echo "Evaluation failed"
    exit 1
fi
```

### Batch Testing

```python
# Load test cases from CSV
import pandas as pd

df = pd.read_csv('test_cases.csv')
test_cases = [
    {'query': row['query'], 'reference_answer': row['answer']}
    for _, row in df.iterrows()
]

results = evaluator.evaluate_dataset(test_cases)
```

---

## 🐛 Troubleshooting

### Error: "PINECONE_API_KEY not found"
**Solution**: Set environment variable:
```bash
export PINECONE_API_KEY='your_key_here'
```

### Error: "No module named 'rouge_score'"
**Solution**: Install missing dependency:
```bash
pip install rouge-score
```

### Error: "Index not found in Pinecone"
**Solution**: Run ingestion first:
```bash
python demo_ingest_pinecone.py
```

### High memory usage
**Solution**: 
- Close other applications
- Use smaller embedding models
- Reduce batch size in evaluation

### Slow evaluation
**Solution**:
- Reduce number of test cases
- Use GPU for embeddings
- Enable caching

---

## 📚 Metric Definitions (Technical)

### BLEU (Bilingual Evaluation Understudy)
- **Formula**: Geometric mean of n-gram precisions (n=1,2,3,4)
- **Range**: 0 to 1
- **Use case**: Machine translation, text generation
- **Limitation**: Doesn't capture semantic meaning

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
- **ROUGE-1**: Unigram overlap
- **ROUGE-2**: Bigram overlap
- **ROUGE-L**: Longest common subsequence
- **Range**: 0 to 1
- **Use case**: Summarization, content coverage

### Semantic Similarity
- **Method**: Cosine similarity of sentence embeddings
- **Model**: sentence-transformers
- **Range**: -1 to 1 (typically 0 to 1)
- **Use case**: Meaning comparison

### Faithfulness
- **Method**: Embedding similarity between answer and context
- **Interpretation**: How grounded the answer is
- **Critical for**: Preventing hallucinations

### Hallucination Detection
- **Method**: Sentence-level context support analysis
- **Formula**: 1 - (average support score)
- **Range**: 0 (no hallucination) to 1 (high hallucination)

---

## 🤝 Contributing

To add new metrics or improve existing ones:

1. Fork the repository
2. Add your metric in `RAGLLMEvaluator` class
3. Update visualizations
4. Add documentation
5. Submit pull request

---

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review console logs for detailed errors
- Ensure all environment variables are set
- Verify Pinecone index is populated

---

## 🎯 Next Steps

1. **Run your first evaluation**: `python evaluate_rag_llm.py`
2. **Review HTML report**: Open in browser
3. **Analyze metrics**: Identify weak areas
4. **Optimize system**: Apply recommendations
5. **Re-evaluate**: Track improvements
6. **Deploy confidently**: With validated performance

---

**Happy Evaluating! 🚀**

Remember: Regular evaluation ensures your RAG system remains accurate, fast, and reliable in production!


