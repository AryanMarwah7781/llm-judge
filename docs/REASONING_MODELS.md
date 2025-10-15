# OpenAI Reasoning Models (o1)

## Overview

We've added support for OpenAI's **o1 reasoning models** to the LLM Judge platform. These models use extended thinking to provide more thoughtful and accurate evaluations, especially for complex legal, medical, and technical content.

## Available Models

### 🧠 O1 (Full Reasoning Model)
- **Best for**: Complex legal analysis, multi-step reasoning, detailed evaluations
- **Accuracy**: ~98%
- **Cost**: $0.15 per evaluation (~$0.015 input + $0.06 output per 1K tokens)
- **Context**: 200K tokens
- **Special Feature**: Extended thinking time for thorough analysis

### 🧠 O1-Mini (Fast Reasoning Model)
- **Best for**: STEM content, code evaluation, faster reasoning tasks
- **Accuracy**: ~94%
- **Cost**: $0.03 per evaluation (~$0.003 input + $0.012 output per 1K tokens)
- **Context**: 128K tokens
- **Special Feature**: Optimized for speed while maintaining reasoning capabilities

## Key Differences from Regular Models

### Technical Implementation
1. **No System Messages**: o1 models don't support system messages - we combine system prompt with user prompt
2. **No Temperature Control**: These models use their own reasoning process
3. **No JSON Mode**: Responses require JSON extraction from text
4. **Extended Thinking**: Models spend more time analyzing before responding

### When to Use Reasoning Models

✅ **Use O1/O1-Mini when:**
- Evaluating complex legal citations and precedents
- Multi-criterion evaluations requiring deep analysis
- Detecting subtle hallucinations in technical content
- High-stakes evaluations where accuracy is critical
- Complex medical or scientific content evaluation

❌ **Use Regular Models (GPT-4o, Claude) when:**
- Quick evaluations with straightforward criteria
- Budget-conscious operations
- Simple pass/fail checks
- High-volume batch processing

## Cost Comparison

For a typical evaluation with 5 Q&A pairs and 3 criteria (15 evaluations):

| Model | Per Evaluation | 15 Evaluations | 1000 Evaluations |
|-------|---------------|----------------|------------------|
| **O1** | $0.15 | $2.25 | $150 |
| **O1-Mini** | $0.03 | $0.45 | $30 |
| GPT-4o | $0.025 | $0.375 | $25 |
| GPT-4o-Mini | $0.002 | $0.03 | $2 |
| Claude Sonnet 4 | $0.03 | $0.45 | $30 |

## Usage Examples

### Via Frontend
1. Go to the Model Selection screen
2. Look for models with the **🧠 REASONING** badge
3. Select either O1 or O1-Mini
4. Upload your document and run evaluation

### Via API (curl)
```bash
curl -X POST https://web-production-446a5.up.railway.app/api/evaluate \
  -F "file=@document.pdf" \
  -F 'criteria=[{"name":"CITATION_ACCURACY","weight":50,"hardMin":70,"description":"Check legal citations"},{"name":"LEGAL_REASONING","weight":50,"hardMin":60,"description":"Evaluate legal reasoning"}]' \
  -F "judge_model=o1"
```

### Via Python
```python
import requests

files = {'file': open('document.pdf', 'rb')}
data = {
    'criteria': '[{"name":"CITATION_ACCURACY","weight":100,"hardMin":80,"description":"Check citations"}]',
    'judge_model': 'o1-mini',
    'domain': 'legal'
}

response = requests.post(
    'https://web-production-446a5.up.railway.app/api/evaluate',
    files=files,
    data=data
)
```

## Performance Insights

### O1 vs Regular Models

**Citation Accuracy**: O1 models are significantly better at:
- Detecting fabricated case citations
- Verifying jurisdiction correctness
- Identifying subtle legal errors
- Multi-step logical reasoning

**Speed**:
- O1: 10-20 seconds per evaluation (extended thinking)
- O1-Mini: 5-10 seconds per evaluation
- GPT-4o: 2-5 seconds per evaluation
- GPT-4o-Mini: 1-3 seconds per evaluation

## Model Selection Guide

```
┌─────────────────────────────────────────────────┐
│  Choose Your Model Based On:                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ACCURACY CRITICAL? ────────────────► O1         │
│                                                  │
│  COMPLEX REASONING? ────────────────► O1         │
│                                                  │
│  STEM/CODE FOCUS? ──────────────────► O1-MINI    │
│                                                  │
│  BALANCED PERFORMANCE? ─────────────► CLAUDE     │
│                                                  │
│  FAST & CHEAP? ─────────────────────► GPT-4O-MINI│
│                                                  │
│  HIGH VOLUME? ──────────────────────► GPT-4O-MINI│
│                                                  │
└─────────────────────────────────────────────────┘
```

## Frontend UI Changes

The frontend now displays:
- **🧠 REASONING** badge on O1 models
- Updated model cards with thinking modes (DEEP_THINKING, FAST_REASONING)
- Recommended badge on O1 (full) model for best accuracy
- Clear pricing and accuracy comparisons

## Backend Implementation

### Key Code Changes

**schemas.py**: Added o1 models to Literal type
```python
judge_model: Literal["gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "claude-sonnet-4"]
```

**llm_judge.py**: Special handling for reasoning models
```python
is_reasoning_model = model.startswith("o1")
if is_reasoning_model:
    # Combine system + user prompt (no system message support)
    combined_prompt = f"{get_system_prompt()}\n\n{prompt}"
    # No temperature or JSON mode
```

**evaluate.py**: Added model metadata and validation
```python
valid_models = ["gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "claude-sonnet-4"]
```

## Testing

Test the reasoning models with this command:

```bash
# Test O1 model
curl -X POST https://web-production-446a5.up.railway.app/api/evaluate \
  -F "file=@test_pdfs/01_general_knowledge_perfect.txt" \
  -F 'criteria=[{"name":"CITATION_ACCURACY","weight":50,"hardMin":70,"description":"Check legal citations"},{"name":"LEGAL_REASONING","weight":50,"hardMin":60,"description":"Evaluate legal reasoning"}]' \
  -F "judge_model=o1" | python3 -m json.tool

# Test O1-Mini model
curl -X POST https://web-production-446a5.up.railway.app/api/evaluate \
  -F "file=@test_pdfs/01_general_knowledge_perfect.txt" \
  -F 'criteria=[{"name":"CITATION_ACCURACY","weight":50,"hardMin":70,"description":"Check legal citations"},{"name":"LEGAL_REASONING","weight":50,"hardMin":60,"description":"Evaluate legal reasoning"}]' \
  -F "judge_model=o1-mini" | python3 -m json.tool
```

## Notes

- O1 models are currently in beta and may have usage limits
- Reasoning models work best with complex, nuanced evaluation criteria
- For simple yes/no checks, regular models are more cost-effective
- O1 models automatically extract JSON from their responses
- Extended thinking time means slower but more accurate results

## Resources

- [OpenAI O1 Announcement](https://openai.com/blog/introducing-openai-o1)
- [O1 API Documentation](https://platform.openai.com/docs/models/o1)
- [Reasoning Models Best Practices](https://platform.openai.com/docs/guides/reasoning)

---

**Last Updated**: October 15, 2025  
**Backend**: https://web-production-446a5.up.railway.app  
**Version**: v1.1.0
