# LLM as Judge - Evaluation API

A production-ready FastAPI backend for evaluating Q&A pairs using multiple LLM judges (OpenAI GPT-4o, Anthropic Claude). This system processes PDF documents containing Q&A pairs, evaluates them against custom criteria, and returns detailed scoring results with pass/fail verdicts.

## 🚀 Features

- **Multi-LLM Support**: Evaluate using GPT-4o, GPT-4o-mini, or Claude Sonnet 4
- **PDF Processing**: Automatic extraction of Q&A pairs from uploaded PDFs
- **Flexible Criteria**: Define custom evaluation criteria with weights and hard minimums
- **Concurrent Evaluation**: Async processing for optimal performance
- **Detailed Results**: Comprehensive scoring with reasoning and issue identification
- **Production Ready**: Error handling, retry logic, logging, and deployment configuration
- **RESTful API**: Clean, well-documented endpoints with OpenAPI/Swagger docs

## 📋 Requirements

- Python 3.10+
- OpenAI API key (for GPT-4o models)
- Anthropic API key (for Claude models)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LLMasjudge
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-13T12:00:00.000Z",
  "api_keys_configured": {
    "openai": true,
    "anthropic": true
  }
}
```

#### 2. Get Available Models
```http
GET /api/models
```

Response:
```json
{
  "models": [
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "provider": "OpenAI",
      "description": "OpenAI's most advanced model...",
      "context_window": 128000,
      "cost_per_1k_tokens": {
        "input": 0.0025,
        "output": 0.010
      }
    }
  ]
}
```

#### 3. Evaluate Q&A Pairs
```http
POST /api/evaluate
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (file): PDF file containing Q&A pairs
- `criteria` (string): JSON array of evaluation criteria
- `judge_model` (string, optional): Judge model to use (default: "gpt-4o")
- `global_threshold` (number, optional): Global pass/fail threshold (default: 85)
- `domain` (string, optional): Domain context (default: "general")

**Example Request (using curl):**
```bash
curl -X POST "http://localhost:8000/api/evaluate" \
  -F "file=@qa_pairs.pdf" \
  -F 'criteria=[
    {
      "name": "CITATION_ACCURACY",
      "weight": 30,
      "hardMin": 70,
      "description": "Accuracy and completeness of citations"
    },
    {
      "name": "RELEVANCE",
      "weight": 25,
      "hardMin": 60,
      "description": "Relevance of answer to question"
    },
    {
      "name": "CLARITY",
      "weight": 25,
      "hardMin": 60,
      "description": "Clarity and readability of answer"
    },
    {
      "name": "COMPLETENESS",
      "weight": 20,
      "hardMin": 65,
      "description": "Completeness of answer"
    }
  ]' \
  -F "judge_model=gpt-4o" \
  -F "global_threshold=85" \
  -F "domain=legal"
```

**Response:**
```json
{
  "evaluations": [
    {
      "qa_id": 1,
      "question": "What is the statute of limitations for...",
      "answer": "The statute of limitations for...",
      "scores": {
        "CITATION_ACCURACY": {
          "score": 85,
          "reasoning": "Citations are accurate and properly formatted...",
          "passed": true,
          "issues": []
        },
        "RELEVANCE": {
          "score": 90,
          "reasoning": "Answer directly addresses the question...",
          "passed": true,
          "issues": []
        },
        "CLARITY": {
          "score": 88,
          "reasoning": "Answer is well-structured and clear...",
          "passed": true,
          "issues": []
        },
        "COMPLETENESS": {
          "score": 82,
          "reasoning": "Answer covers main points but could include...",
          "passed": true,
          "issues": ["Missing discussion of exceptions"]
        }
      },
      "weighted_score": 86.25,
      "verdict": "PASS",
      "reason": null
    }
  ],
  "summary": {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "avg_score": 86.25
  }
}
```

## 🏗️ Architecture

### Project Structure

```
LLMasjudge/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app setup
│   ├── config.py            # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── evaluate.py      # Evaluation endpoints
│   │   └── health.py        # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py    # PDF parsing
│   │   ├── llm_judge.py     # LLM API integration
│   │   ├── criteria.py      # Criteria validation
│   │   └── evaluator.py     # Evaluation orchestration
│   └── utils/
│       ├── __init__.py
│       └── prompts.py       # Judge prompt templates
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile                 # Deployment configuration
└── README.md
```

### Key Design Decisions

1. **Async/Await Throughout**: All I/O operations are async for maximum concurrency
2. **Service Layer Pattern**: Business logic separated into services for maintainability
3. **Pydantic Validation**: Strong type checking and validation at API boundaries
4. **Retry Logic**: Exponential backoff for LLM API calls to handle transient failures
5. **Error Handling**: Comprehensive error handling with clear user-facing messages
6. **Concurrent Evaluation**: Multiple Q&As and criteria evaluated in parallel
7. **Configuration Management**: Environment-based configuration with sensible defaults

## 🎯 Evaluation Logic

### Evaluation Flow

1. **PDF Upload**: User uploads PDF with Q&A pairs
2. **Parsing**: Extract Q&A pairs using PyMuPDF4LLM
3. **Concurrent Evaluation**: For each Q&A pair:
   - Evaluate all criteria concurrently
   - Each criterion gets scored 0-100 with reasoning
4. **Score Calculation**:
   - Check hard minimums (instant fail if below threshold)
   - Calculate weighted average score
   - Apply global threshold
5. **Verdict**: Determine PASS/REJECT with reason

### Criteria Structure

Each criterion must include:
- `name`: Unique identifier (e.g., "CITATION_ACCURACY")
- `weight`: Percentage weight (all weights must sum to 100)
- `hardMin`: Minimum acceptable score (0-100)
- `description`: What this criterion measures

### Verdict Logic

A Q&A pair **FAILS** if:
1. Any criterion scores below its hard minimum, OR
2. Weighted average score is below global threshold

Otherwise, it **PASSES**.

## 🌐 Deployment

### Railway / Render

1. Connect your repository
2. Set environment variables:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `ENVIRONMENT=production`
3. The `Procfile` is already configured
4. Deploy!

### Docker (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t llm-judge-api .
docker run -p 8000:8000 --env-file .env llm-judge-api
```

## 🧪 Testing

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/api/health

# Get models
curl http://localhost:8000/api/models

# Evaluate (see API Documentation section for full example)
```

### Python Testing

```python
import requests

# Prepare data
files = {"file": open("qa_pairs.pdf", "rb")}
data = {
    "criteria": '[{"name": "ACCURACY", "weight": 100, "hardMin": 70, "description": "Answer accuracy"}]',
    "judge_model": "gpt-4o",
    "global_threshold": 85,
    "domain": "general"
}

# Make request
response = requests.post(
    "http://localhost:8000/api/evaluate",
    files=files,
    data=data
)

print(response.json())
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key |
| `ENVIRONMENT` | No | production | Environment (development/production) |
| `LOG_LEVEL` | No | INFO | Logging level |
| `GLOBAL_THRESHOLD` | No | 85 | Default global threshold |
| `ALLOWED_ORIGINS` | No | localhost:3000,localhost:5173 | CORS origins |
| `MAX_RETRIES` | No | 3 | Max API retry attempts |
| `RETRY_DELAY` | No | 1 | Initial retry delay (seconds) |

*At least one API key (OpenAI or Anthropic) is required

## 📊 Performance

- **Concurrent Evaluation**: Multiple Q&As and criteria evaluated in parallel
- **Retry Logic**: Automatic retry with exponential backoff
- **Async I/O**: Non-blocking operations throughout
- **Efficient Parsing**: Fast PDF extraction with PyMuPDF

### Typical Latency

- 1 Q&A, 4 criteria: ~5-10 seconds
- 10 Q&As, 4 criteria: ~15-25 seconds (concurrent)
- Varies by LLM provider and model

## 🐛 Troubleshooting

### Common Issues

**1. "API key not configured"**
- Ensure `.env` file exists and contains valid API keys
- Check that keys don't still have placeholder values

**2. "No Q&A pairs found in PDF"**
- Ensure PDF has clear Q&A structure
- Supported formats: "Q: ... A: ...", "Question: ... Answer: ...", numbered pairs

**3. "Criteria weights must sum to 100"**
- Verify all criterion weights add up to exactly 100

**4. Rate Limit Errors**
- System will automatically retry with exponential backoff
- Consider using lower-tier models for testing

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review API logs for error details

## 🚀 Roadmap

- [ ] Add caching for repeated evaluations
- [ ] Support for additional LLM providers
- [ ] Batch evaluation endpoints
- [ ] Webhook support for long-running evaluations
- [ ] Dashboard UI for monitoring
- [ ] Export results to various formats (CSV, JSON, PDF)

---

Built with ❤️ using FastAPI, OpenAI, and Anthropic
