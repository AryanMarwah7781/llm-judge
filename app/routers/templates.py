"""Template management endpoints."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.template_manager import template_manager
from app.models.schemas import Criterion


router = APIRouter(prefix="/api/templates", tags=["templates"])


class CreateTemplateRequest(BaseModel):
    """Request to create a new template."""
    name: str = Field(..., description="Template name", min_length=1)
    domain: str = Field(..., description="Domain (legal, medical, finance, general)")
    criteria: List[Criterion] = Field(..., description="Evaluation criteria")
    description: Optional[str] = Field(None, description="Template description")


class UpdateTemplateRequest(BaseModel):
    """Request to update a template."""
    name: Optional[str] = Field(None, description="New template name")
    domain: Optional[str] = Field(None, description="New domain")
    criteria: Optional[List[Criterion]] = Field(None, description="New criteria")
    description: Optional[str] = Field(None, description="New description")


class TemplateResponse(BaseModel):
    """Template response."""
    id: str
    name: str
    domain: str
    description: str
    criteria: List[Criterion]
    created_at: str
    updated_at: str


class TemplateListResponse(BaseModel):
    """List of templates."""
    templates: List[TemplateResponse]


@router.post("", response_model=TemplateResponse, status_code=201)
async def create_template(request: CreateTemplateRequest) -> TemplateResponse:
    """
    Create a new criteria template.

    Args:
        request: Template creation request

    Returns:
        Created template with ID

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Convert criteria to dict format
        criteria_dicts = [c.model_dump() for c in request.criteria]

        template = template_manager.save_template(
            name=request.name,
            domain=request.domain,
            criteria=criteria_dicts,
            description=request.description
        )

        # Convert back to response model
        template["criteria"] = [Criterion(**c) for c in template["criteria"]]
        return TemplateResponse(**template)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create template: {str(e)}"
        )


@router.get("", response_model=TemplateListResponse)
async def list_templates(domain: Optional[str] = None) -> TemplateListResponse:
    """
    List all templates, optionally filtered by domain.

    Args:
        domain: Optional domain filter (legal, medical, finance, general)

    Returns:
        List of templates
    """
    try:
        templates = template_manager.list_templates(domain=domain)

        # Convert criteria to Criterion objects
        for template in templates:
            template["criteria"] = [Criterion(**c) for c in template["criteria"]]

        return TemplateListResponse(
            templates=[TemplateResponse(**t) for t in templates]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list templates: {str(e)}"
        )


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str) -> TemplateResponse:
    """
    Get a specific template by ID.

    Args:
        template_id: Template ID

    Returns:
        Template details

    Raises:
        HTTPException: If template not found
    """
    template = template_manager.get_template(template_id)

    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found: {template_id}"
        )

    # Convert criteria to Criterion objects
    template["criteria"] = [Criterion(**c) for c in template["criteria"]]

    return TemplateResponse(**template)


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    request: UpdateTemplateRequest
) -> TemplateResponse:
    """
    Update an existing template.

    Args:
        template_id: Template ID
        request: Update request

    Returns:
        Updated template

    Raises:
        HTTPException: If template not found or update fails
    """
    try:
        # Convert criteria to dict if provided
        criteria_dicts = None
        if request.criteria:
            criteria_dicts = [c.model_dump() for c in request.criteria]

        template = template_manager.update_template(
            template_id=template_id,
            name=request.name,
            domain=request.domain,
            criteria=criteria_dicts,
            description=request.description
        )

        if not template:
            raise HTTPException(
                status_code=404,
                detail=f"Template not found: {template_id}"
            )

        # Convert criteria back to Criterion objects
        template["criteria"] = [Criterion(**c) for c in template["criteria"]]

        return TemplateResponse(**template)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update template: {str(e)}"
        )


@router.delete("/{template_id}", status_code=204)
async def delete_template(template_id: str):
    """
    Delete a template.

    Args:
        template_id: Template ID

    Raises:
        HTTPException: If template not found
    """
    success = template_manager.delete_template(template_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found: {template_id}"
        )

    return None
