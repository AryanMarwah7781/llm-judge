# Project Structure

```
LLMasjudge/
├── 📄 README.md                    # Comprehensive documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 DESIGN.md                    # Architecture & design decisions
├── 📄 PROJECT_SUMMARY.md           # This summary document
├── 📄 DOCKER.md                    # Docker deployment guide
├── 📄 LICENSE                      # MIT License
│
├── 📦 requirements.txt             # Python dependencies
├── 🔧 .env.example                 # Environment template
├── 🚫 .gitignore                   # Git ignore rules
├── 🚀 Procfile                     # Railway/Render deployment
├── 🐳 Dockerfile                   # Docker configuration
├── 🐳 docker-compose.yml           # Docker Compose setup
│
├── 🧪 verify_setup.py              # Installation verification
├── 📝 example_usage.py             # API usage examples
├── 📋 sample_qa_pairs.md           # Test data examples
│
└── 📁 app/                         # Main application
    ├── __init__.py
    ├── main.py                     # FastAPI app setup & config
    ├── config.py                   # Settings & environment
    │
    ├── 📁 models/                  # Data models
    │   ├── __init__.py
    │   └── schemas.py              # Pydantic models
    │
    ├── 📁 routers/                 # API endpoints
    │   ├── __init__.py
    │   ├── evaluate.py             # Evaluation endpoints
    │   └── health.py               # Health check
    │
    ├── 📁 services/                # Business logic
    │   ├── __init__.py
    │   ├── pdf_parser.py           # PDF parsing
    │   ├── llm_judge.py            # LLM API integration
    │   ├── criteria.py             # Criteria validation
    │   └── evaluator.py            # Evaluation orchestration
    │
    └── 📁 utils/                   # Utilities
        ├── __init__.py
        └── prompts.py              # Prompt templates
```

## File Descriptions

### 📚 Documentation (7 files)
- **README.md** - Main documentation with installation, API docs, examples
- **QUICKSTART.md** - Get running in 5 minutes
- **DESIGN.md** - Architecture decisions and patterns
- **PROJECT_SUMMARY.md** - Complete overview of what was built
- **DOCKER.md** - Container deployment instructions
- **LICENSE** - MIT license
- **sample_qa_pairs.md** - Example Q&A pairs for testing

### ⚙️ Configuration (6 files)
- **requirements.txt** - All Python dependencies with versions
- **.env.example** - Environment variable template
- **.gitignore** - Git ignore patterns
- **Procfile** - Deploy to Railway/Render
- **Dockerfile** - Build container image
- **docker-compose.yml** - Local development with Docker

### 🛠️ Utilities (2 files)
- **verify_setup.py** - Check installation and configuration
- **example_usage.py** - Working examples of API usage

### 🚀 Application Core (14 files)

#### Main Application (2 files)
- **app/main.py** - FastAPI app, middleware, exception handlers
- **app/config.py** - Configuration management with Pydantic

#### Models (1 file)
- **app/models/schemas.py** - All Pydantic models for validation

#### Routers (2 files)
- **app/routers/evaluate.py** - POST /api/evaluate, GET /api/models
- **app/routers/health.py** - GET /api/health

#### Services (4 files)
- **app/services/pdf_parser.py** - Extract Q&A pairs from PDFs
- **app/services/llm_judge.py** - Call OpenAI/Anthropic APIs
- **app/services/criteria.py** - Validate criteria & calculate scores
- **app/services/evaluator.py** - Orchestrate full evaluation flow

#### Utils (1 file)
- **app/utils/prompts.py** - LLM judge prompt templates

## Total Files: 29

### Breakdown by Type:
- **Python Code**: 14 files
- **Documentation**: 7 files
- **Configuration**: 6 files
- **Utilities**: 2 files

## Lines of Code (Approximate):
- **Python**: ~2,500 lines
- **Documentation**: ~1,500 lines
- **Configuration**: ~100 lines
- **Total**: ~4,100 lines

## Key Features by File:

### app/main.py
- FastAPI setup
- CORS middleware
- Exception handlers
- Startup/shutdown events
- Route registration

### app/services/evaluator.py
- Concurrent Q&A evaluation
- Concurrent criteria evaluation
- Error handling with partial success
- Summary statistics

### app/services/llm_judge.py
- OpenAI integration
- Anthropic integration
- Retry logic with exponential backoff
- JSON response parsing

### app/services/pdf_parser.py
- Multi-pattern Q&A extraction
- Text cleaning and validation
- Temporary file handling

### app/routers/evaluate.py
- File upload handling
- Criteria parsing and validation
- Model selection
- Error responses

## Dependencies:

### Core Framework:
- fastapi - Web framework
- uvicorn - ASGI server
- pydantic - Data validation

### LLM Integration:
- openai - OpenAI API
- anthropic - Anthropic API
- tenacity - Retry logic

### PDF Processing:
- pymupdf4llm - PDF parsing
- pymupdf - PDF library

### Utilities:
- python-multipart - File uploads
- python-dotenv - Environment variables
- aiofiles - Async file operations

## Architecture Patterns Used:

1. **Layered Architecture**
   - API → Router → Service → Integration

2. **Service Layer Pattern**
   - Business logic in services/
   - Reusable and testable

3. **Dependency Injection**
   - Configuration via settings
   - Service instances

4. **Async/Await**
   - Throughout the stack
   - Concurrent execution

5. **Factory Pattern**
   - LLM client creation
   - Model-specific handlers

## Testing Structure (Recommended):

```
tests/
├── unit/
│   ├── test_criteria.py
│   ├── test_pdf_parser.py
│   └── test_evaluator.py
├── integration/
│   ├── test_api.py
│   └── test_llm_judge.py
└── e2e/
    └── test_full_flow.py
```

## Deployment Targets:

✅ Railway
✅ Render
✅ Docker (any platform)
✅ AWS ECS
✅ Google Cloud Run
✅ Azure Container Apps
✅ Kubernetes

## Development Workflow:

1. **Setup**: `python verify_setup.py`
2. **Run**: `uvicorn app.main:app --reload`
3. **Test**: Visit http://localhost:8000/docs
4. **Deploy**: Push to GitHub → Connect to platform
5. **Monitor**: Check logs and health endpoint

## Performance Characteristics:

- **Latency**: 5-40s depending on Q&A count
- **Throughput**: Limited by LLM API rate limits
- **Concurrency**: Efficient async I/O
- **Memory**: Low footprint (~100-200MB)
- **CPU**: Minimal (mostly I/O bound)

## Security Features:

- Environment-based secrets
- Input validation (Pydantic)
- File type checking
- Temporary file cleanup
- Non-root Docker user
- CORS configuration
- Error message sanitization

---

**This structure represents a production-ready FastAPI application with clean architecture, comprehensive documentation, and multiple deployment options.**
