"""Pydantic schemas for request and response models."""
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class Criterion(BaseModel):
    """Evaluation criterion with weight and hard minimum."""
    name: str = Field(..., description="Criterion name (e.g., CITATION_ACCURACY)")
    weight: float = Field(..., ge=0, le=100, description="Weight percentage (0-100)")
    hardMin: float = Field(..., ge=0, le=100, description="Hard minimum threshold (0-100)")
    description: str = Field(..., description="Description of what this criterion measures")


class EvaluationRequest(BaseModel):
    """Request model for evaluation endpoint (from form data)."""
    criteria: List[Criterion]
    judge_model: Literal["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"] = Field(
        default="gpt-4o",
        description="LLM judge model to use"
    )
    global_threshold: float = Field(
        default=85,
        ge=0,
        le=100,
        description="Global threshold for pass/fail (0-100)"
    )
    domain: Optional[str] = Field(
        default="general",
        description="Domain context (legal, medical, finance, general)"
    )

    @field_validator("criteria")
    @classmethod
    def validate_criteria_weights(cls, v: List[Criterion]) -> List[Criterion]:
        """Ensure criteria weights sum to 100."""
        if not v:
            raise ValueError("At least one criterion is required")
        
        total_weight = sum(c.weight for c in v)
        if abs(total_weight - 100) > 0.01:  # Allow for floating point errors
            raise ValueError(f"Criteria weights must sum to 100, got {total_weight}")
        
        return v


class QAPair(BaseModel):
    """Question-answer pair extracted from PDF."""
    qa_id: int = Field(..., description="Unique identifier for this Q&A pair")
    question: str = Field(..., description="The question text")
    answer: str = Field(..., description="The answer text")


class CriterionScore(BaseModel):
    """Score result for a single criterion."""
    score: float = Field(..., ge=0, le=100, description="Score from 0-100")
    reasoning: str = Field(..., description="Explanation for the score")
    passed: bool = Field(..., description="Whether the hard minimum was met")
    issues: Optional[List[str]] = Field(default=None, description="Specific issues found")


class QAEvaluation(BaseModel):
    """Evaluation results for a single Q&A pair."""
    qa_id: int
    question: str
    answer: str
    scores: Dict[str, CriterionScore] = Field(..., description="Scores for each criterion")
    weighted_score: float = Field(..., ge=0, le=100, description="Weighted average score")
    verdict: Literal["PASS", "REJECT"] = Field(..., description="Final pass/fail verdict")
    reason: Optional[str] = Field(None, description="Reason for rejection if applicable")


class EvaluationSummary(BaseModel):
    """Summary statistics for all evaluations."""
    total: int = Field(..., description="Total number of Q&A pairs evaluated")
    passed: int = Field(..., description="Number of Q&A pairs that passed")
    failed: int = Field(..., description="Number of Q&A pairs that failed")
    avg_score: float = Field(..., description="Average weighted score across all pairs")


class SafetyWarning(BaseModel):
    """Safety warning for a Q&A pair."""
    type: str = Field(..., description="Warning type (manipulation, bias)")
    severity: str = Field(..., description="Severity level (high, medium, low)")
    score: float = Field(..., description="Detection confidence score")
    description: str = Field(..., description="Human-readable warning description")
    categories: Optional[List[str]] = Field(None, description="Affected categories (for bias)")
    attacks: Optional[List[str]] = Field(None, description="Detected attack types (for manipulation)")


class QASafetyWarnings(BaseModel):
    """Safety warnings for a specific Q&A pair."""
    qa_index: int = Field(..., description="Index of the Q&A pair")
    question: str = Field(..., description="Question preview")
    warnings: List[SafetyWarning] = Field(..., description="List of warnings")


class EvaluationResponse(BaseModel):
    """Complete evaluation response."""
    evaluations: List[QAEvaluation] = Field(..., description="Individual Q&A evaluations")
    summary: EvaluationSummary = Field(..., description="Summary statistics")
    safety_warnings: Optional[List[QASafetyWarnings]] = Field(default=[], description="Safety warnings from lightweight checks")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
    api_keys_configured: Dict[str, bool] = Field(..., description="API key configuration status")


class JudgeModel(BaseModel):
    """Available judge model information."""
    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name")
    provider: str = Field(..., description="Provider (OpenAI, Anthropic)")
    description: str = Field(..., description="Model description")
    context_window: int = Field(..., description="Maximum context window size")
    cost_per_1k_tokens: Dict[str, float] = Field(..., description="Cost structure")


class ModelsResponse(BaseModel):
    """Available models response."""
    models: List[JudgeModel] = Field(..., description="List of available judge models")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
