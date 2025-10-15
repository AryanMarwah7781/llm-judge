# LLM as Judge - Design Document

## Overview

This document outlines the key architectural decisions and design patterns used in the LLM as Judge evaluation platform.

## Core Architecture

### 1. Layered Architecture

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)          │  ← HTTP endpoints, validation
├─────────────────────────────────────┤
│      Router Layer (Endpoints)        │  ← Request handling, routing
├─────────────────────────────────────┤
│      Service Layer (Business Logic)  │  ← Core evaluation logic
├─────────────────────────────────────┤
│   Integration Layer (External APIs)  │  ← LLM providers, PDF parsing
└─────────────────────────────────────┘
```

**Benefits:**
- Clear separation of concerns
- Testability at each layer
- Easy to modify one layer without affecting others
- Scalable and maintainable

### 2. Async/Await Throughout

**Decision:** Use async/await for all I/O operations

**Rationale:**
- LLM API calls can take 5-15 seconds each
- Multiple Q&A pairs can be evaluated concurrently
- Multiple criteria per Q&A can be evaluated concurrently
- Async allows single process to handle multiple requests efficiently

**Implementation:**
```python
async def evaluate_qa_pairs(qa_pairs, criteria):
    # Evaluate all Q&A pairs concurrently
    tasks = [evaluate_single_qa(qa) for qa in qa_pairs]
    return await asyncio.gather(*tasks)
```

**Performance Impact:**
- 10 Q&As with 4 criteria each = 40 sequential LLM calls (~400s)
- With async: ~30-40s (10x improvement)

### 3. Service Layer Pattern

**Services:**
- `pdf_parser.py` - PDF processing and Q&A extraction
- `llm_judge.py` - LLM API integration with retry logic
- `criteria.py` - Criteria validation and scoring logic
- `evaluator.py` - Orchestration of evaluation workflow

**Benefits:**
- Single responsibility principle
- Reusable business logic
- Easy to unit test
- Clear dependencies

### 4. Pydantic Models

**Decision:** Use Pydantic for all data validation

**Benefits:**
- Type safety at runtime
- Automatic validation
- Clear API contracts
- Great documentation generation
- JSON serialization/deserialization

**Example:**
```python
class Criterion(BaseModel):
    name: str
    weight: float = Field(ge=0, le=100)
    hardMin: float = Field(ge=0, le=100)
    description: str
    
    @field_validator("criteria")
    def validate_weights(cls, v):
        if sum(c.weight for c in v) != 100:
            raise ValueError("Weights must sum to 100")
        return v
```

## Key Design Decisions

### 1. Retry Logic with Exponential Backoff

**Problem:** LLM APIs can fail due to:
- Rate limits
- Temporary network issues
- Service availability

**Solution:** Tenacity library with exponential backoff

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_llm_api():
    # API call
```

**Benefits:**
- Automatic recovery from transient failures
- Respects rate limits
- Configurable retry strategy

### 2. Concurrent Evaluation Strategy

**Two Levels of Concurrency:**

1. **Q&A Level:** Evaluate all Q&A pairs concurrently
2. **Criterion Level:** Evaluate all criteria for each Q&A concurrently

```python
# Level 1: Concurrent Q&As
qa_tasks = [evaluate_qa(qa) for qa in qa_pairs]
results = await asyncio.gather(*qa_tasks)

# Level 2: Concurrent criteria (within each Q&A)
criterion_tasks = [evaluate_criterion(c) for c in criteria]
scores = await asyncio.gather(*criterion_tasks)
```

**Why Two Levels?**
- Maximizes parallelism
- Minimizes total evaluation time
- Efficient use of async capabilities

### 3. Error Handling Strategy

**Approach:** Fail gracefully at Q&A level, not batch level

**Rationale:**
- If one Q&A fails, others should still be evaluated
- Return partial results rather than complete failure
- Provide detailed error information per Q&A

**Implementation:**
```python
evaluations = await asyncio.gather(*tasks, return_exceptions=True)
for result in evaluations:
    if isinstance(result, Exception):
        # Create failed evaluation with error details
        failed_evaluations.append(create_failed_eval(result))
    else:
        successful_evaluations.append(result)
```

### 4. PDF Parsing Strategy

**Multi-Pattern Matching:**

Support multiple Q&A formats:
- `Q: ... A: ...`
- `Question: ... Answer: ...`
- `**Q:** ... **A:** ...` (bold)
- Numbered format with separation

**Rationale:**
- PDFs vary widely in format
- Increase success rate of extraction
- User-friendly (less formatting requirements)

**Validation:**
- Minimum length checks
- Question indicators detection
- Prevent duplicate detection

### 5. Prompt Engineering

**Structured Approach:**

1. **System Prompt:** Defines role and expectations
2. **Domain Context:** Provides domain-specific guidance
3. **Evaluation Instructions:** Clear scoring guidelines
4. **JSON Response Format:** Enforced structure

**Key Elements:**
```
- Role definition
- Domain context (legal/medical/etc)
- Clear scoring rubric (0-20, 21-40, etc)
- Specific output format requirement
- Examples of issues to look for
```

**Benefits:**
- Consistent evaluation quality
- Structured responses
- Easy to parse results
- Domain-specific expertise

### 6. Configuration Management

**Decision:** Environment-based configuration with Pydantic Settings

**Structure:**
```python
class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    environment: str = "production"
    
    model_config = SettingsConfigDict(env_file=".env")
```

**Benefits:**
- Type-safe configuration
- Environment variable support
- Validation at startup
- Easy to test with different configs

### 7. API Response Structure

**Comprehensive Response Design:**

```json
{
  "evaluations": [...],  // Individual results
  "summary": {           // Aggregate statistics
    "total": 10,
    "passed": 7,
    "failed": 3,
    "avg_score": 81.5
  }
}
```

**Rationale:**
- Clients get both detail and overview
- Easy to display in UI
- Supports different client needs
- Self-contained responses

## Performance Optimizations

### 1. Concurrent API Calls
- Multiple LLM calls in parallel
- Reduces total evaluation time by ~10x

### 2. Async I/O
- Non-blocking file operations
- Non-blocking HTTP requests
- Single process handles multiple requests

### 3. Efficient PDF Parsing
- Stream processing where possible
- Temporary file cleanup
- Minimal memory footprint

### 4. JSON Response Format
- OpenAI: Use `response_format={"type": "json_object"}`
- Anthropic: Parse JSON from text
- Reduces parsing errors
- Faster processing

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Can run multiple instances behind load balancer
- No shared state between requests

### Vertical Scaling
- Async architecture efficient with resources
- Can handle many concurrent requests per instance
- Limited mainly by LLM API rate limits

### Future Enhancements

1. **Caching Layer**
   - Cache repeated Q&A evaluations
   - Redis or in-memory cache
   - Significant cost savings

2. **Database Layer**
   - Store evaluation history
   - Analytics and reporting
   - Audit trail

3. **Queue System**
   - For large batch evaluations
   - Background processing
   - Progress tracking

4. **Rate Limiting**
   - Protect against abuse
   - Manage API costs
   - Fair usage across clients

## Security Considerations

### 1. API Key Management
- Environment variables only
- Never commit to version control
- Rotate keys regularly

### 2. File Upload Validation
- File type checking
- Size limits
- Temporary file cleanup

### 3. Input Validation
- Pydantic validation on all inputs
- SQL injection not applicable (no SQL)
- XSS not applicable (API only)

### 4. Error Messages
- Production mode hides internal details
- Development mode shows full errors
- No sensitive data in logs

## Testing Strategy

### Unit Tests (Recommended)
- Test each service independently
- Mock external dependencies
- Test edge cases and error handling

### Integration Tests (Recommended)
- Test full evaluation flow
- Use test API keys
- Verify response formats

### End-to-End Tests (Recommended)
- Test with real PDFs
- Test with real LLM APIs
- Verify actual behavior

### Example Test Structure:
```python
# Unit test
def test_criteria_validation():
    criteria = [Criterion(name="TEST", weight=100, ...)]
    assert validate_criteria(criteria) == True

# Integration test
async def test_full_evaluation():
    result = await evaluator.evaluate_qa_pairs(...)
    assert result.summary.total > 0
```

## Monitoring and Observability

### Logging
- Structured logging with levels
- Request/response logging
- Error tracking with stack traces

### Metrics (Future)
- Request count
- Response times
- Error rates
- LLM API costs

### Health Checks
- `/api/health` endpoint
- API key validation
- Version information

## Cost Management

### API Cost Considerations
1. **Model Selection**
   - GPT-4o: Higher quality, higher cost
   - GPT-4o-mini: Faster, cheaper
   - Claude: Balance of quality and cost

2. **Token Usage**
   - Prompts optimized for clarity
   - JSON format reduces output tokens
   - Concurrent calls don't reduce per-call cost

3. **Error Handling**
   - Retry logic limits wasted calls
   - Validation before API calls
   - Cache results where applicable

### Example Costs
- GPT-4o: ~$0.025 per Q&A (4 criteria)
- GPT-4o-mini: ~$0.002 per Q&A (4 criteria)
- Claude Sonnet 4: ~$0.030 per Q&A (4 criteria)

## Deployment Architecture

```
┌─────────────────┐
│   Load Balancer  │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│ App1 │  │ App2 │  ← Multiple instances
└───┬──┘  └──┬───┘
    │        │
    └────┬───┘
         │
    ┌────▼─────┐
    │  LLM APIs │
    └──────────┘
```

## Conclusion

This architecture provides:
- **Performance:** Concurrent evaluation, async I/O
- **Reliability:** Retry logic, error handling
- **Maintainability:** Clean separation of concerns
- **Scalability:** Stateless, horizontally scalable
- **Production-Ready:** Comprehensive error handling, logging, configuration

The design balances simplicity with robustness, making it suitable for production deployment while remaining maintainable and extensible.
