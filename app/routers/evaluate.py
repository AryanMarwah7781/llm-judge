"""Evaluation endpoints."""
import json
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.models.schemas import (
    EvaluationResponse,
    ModelsResponse,
    JudgeModel,
    Criterion,
    ErrorResponse
)
from app.services.pdf_parser import parse_pdf
from app.services.evaluator import evaluator
from app.config import settings

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def evaluate(
    file: UploadFile = File(..., description="PDF or TXT file containing Q&A pairs"),
    criteria: str = Form(..., description="JSON string of evaluation criteria"),
    judge_model: str = Form(default="gpt-4o", description="Judge model to use"),
    global_threshold: float = Form(default=85, ge=0, le=100, description="Global pass/fail threshold"),
    domain: str = Form(default="general", description="Domain context")
) -> EvaluationResponse:
    """
    Evaluate Q&A pairs from PDF or TXT file using LLM judge.
    
    Args:
        file: PDF or TXT file containing Q&A pairs
        criteria: JSON string with evaluation criteria
        judge_model: LLM judge model (gpt-4o, gpt-4o-mini, o1, o1-mini, claude-sonnet-4)
        global_threshold: Global threshold for pass/fail (0-100)
        domain: Domain context (legal, medical, finance, general)
        
    Returns:
        Evaluation results with scores and verdicts
        
    Raises:
        HTTPException: If validation or processing fails
    """
    try:
        # Parse criteria JSON
        try:
            criteria_list = json.loads(criteria)
            criteria_objects = [Criterion(**c) for c in criteria_list]
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid criteria JSON: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid criteria format: {str(e)}"
            )
        
        # Validate judge model
        valid_models = ["gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "claude-sonnet-4"]
        if judge_model not in valid_models:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid judge model. Must be one of: {', '.join(valid_models)}"
            )
        
        # Check if API key is configured for selected model
        if (judge_model.startswith("gpt-") or judge_model.startswith("o1")) and not settings.has_openai_key():
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        if judge_model.startswith("claude-") and not settings.has_anthropic_key():
            raise HTTPException(
                status_code=500,
                detail="Anthropic API key not configured. Please set ANTHROPIC_API_KEY environment variable."
            )
        
        # Parse PDF
        qa_pairs = await parse_pdf(file)
        
        # Evaluate Q&A pairs
        results = await evaluator.evaluate_qa_pairs(
            qa_pairs=qa_pairs,
            criteria=criteria_objects,
            judge_model=judge_model,
            global_threshold=global_threshold,
            domain=domain
        )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/models", response_model=ModelsResponse)
async def get_models() -> ModelsResponse:
    """
    Get available judge models.
    
    Returns:
        List of available judge models with metadata
    """
    models = [
        JudgeModel(
            id="gpt-4o",
            name="GPT-4o",
            provider="OpenAI",
            description="OpenAI's most advanced model with excellent reasoning capabilities",
            context_window=128000,
            cost_per_1k_tokens={
                "input": 0.0025,
                "output": 0.010
            }
        ),
        JudgeModel(
            id="gpt-4o-mini",
            name="GPT-4o Mini",
            provider="OpenAI",
            description="Faster and more cost-effective version of GPT-4o",
            context_window=128000,
            cost_per_1k_tokens={
                "input": 0.00015,
                "output": 0.0006
            }
        ),
        JudgeModel(
            id="o1",
            name="O1",
            provider="OpenAI",
            description="OpenAI's reasoning model with extended thinking for complex analysis",
            context_window=200000,
            cost_per_1k_tokens={
                "input": 0.015,
                "output": 0.060
            }
        ),
        JudgeModel(
            id="o1-mini",
            name="O1 Mini",
            provider="OpenAI",
            description="Faster reasoning model optimized for STEM and code tasks",
            context_window=128000,
            cost_per_1k_tokens={
                "input": 0.003,
                "output": 0.012
            }
        ),
        JudgeModel(
            id="claude-sonnet-4",
            name="Claude Sonnet 4",
            provider="Anthropic",
            description="Anthropic's latest model with superior analysis and reasoning",
            context_window=200000,
            cost_per_1k_tokens={
                "input": 0.003,
                "output": 0.015
            }
        )
    ]
    
    return ModelsResponse(models=models)
