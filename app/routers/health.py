"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

from app.models.schemas import HealthResponse
from app.config import settings

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        Service health status and configuration
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        api_keys_configured={
            "openai": settings.has_openai_key(),
            "anthropic": settings.has_anthropic_key()
        }
    )
