"""LLM judge service for evaluating Q&A pairs."""
import json
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from fastapi import HTTPException

from app.config import settings
from app.utils.prompts import get_evaluation_prompt, get_system_prompt


class LLMJudge:
    """LLM Judge service for evaluating answers."""
    
    def __init__(self):
        """Initialize LLM clients."""
        self.openai_client: Optional[AsyncOpenAI] = None
        self.anthropic_client: Optional[AsyncAnthropic] = None
        
        # Initialize clients lazily to avoid initialization errors
        self._openai_initialized = False
        self._anthropic_initialized = False
    
    def _get_openai_client(self) -> AsyncOpenAI:
        """Get or initialize OpenAI client."""
        if not self._openai_initialized and settings.has_openai_key():
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
            self._openai_initialized = True
        return self.openai_client
    
    def _get_anthropic_client(self) -> AsyncAnthropic:
        """Get or initialize Anthropic client."""
        if not self._anthropic_initialized and settings.has_anthropic_key():
            # Initialize Anthropic client with just the API key
            self.anthropic_client = AsyncAnthropic(
                api_key=settings.anthropic_api_key
            )
            self._anthropic_initialized = True
        return self.anthropic_client
    
    async def evaluate_criterion(
        self,
        question: str,
        answer: str,
        criterion_name: str,
        criterion_description: str,
        domain: str,
        judge_model: str
    ) -> Dict[str, Any]:
        """
        Evaluate answer against a single criterion using LLM judge.
        
        Args:
            question: Question text
            answer: Answer text
            criterion_name: Name of criterion
            criterion_description: Description of criterion
            domain: Domain context
            judge_model: Model to use for evaluation
            
        Returns:
            Dict with score, reasoning, and issues
            
        Raises:
            HTTPException: If evaluation fails
        """
        prompt = get_evaluation_prompt(
            domain=domain,
            question=question,
            answer=answer,
            criterion_name=criterion_name,
            criterion_description=criterion_description
        )
        
        if judge_model.startswith("gpt-"):
            return await self._evaluate_with_openai(prompt, judge_model)
        elif judge_model.startswith("claude-"):
            return await self._evaluate_with_anthropic(prompt, judge_model)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported judge model: {judge_model}"
            )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def _evaluate_with_openai(
        self,
        prompt: str,
        model: str
    ) -> Dict[str, Any]:
        """
        Evaluate using OpenAI API with retry logic.
        
        Args:
            prompt: Evaluation prompt
            model: OpenAI model name
            
        Returns:
            Parsed evaluation result
        """
        client = self._get_openai_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        try:
            # o1 models don't support system messages or temperature
            is_reasoning_model = model.startswith("o1")
            
            if is_reasoning_model:
                # For o1 models: combine system prompt with user prompt
                combined_prompt = f"{get_system_prompt()}\n\n{prompt}"
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": combined_prompt}
                    ]
                )
            else:
                # For regular models: use system message and temperature
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,  # Lower temperature for consistency
                    response_format={"type": "json_object"}
                )
            
            result = response.choices[0].message.content
            
            # For o1 models, we might need to extract JSON from the response
            if is_reasoning_model:
                result = self._extract_json(result)
            
            parsed = json.loads(result)
            
            return self._validate_and_normalize_result(parsed)
            
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse LLM response as JSON: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI API error: {str(e)}"
            )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def _evaluate_with_anthropic(
        self,
        prompt: str,
        model: str
    ) -> Dict[str, Any]:
        """
        Evaluate using Anthropic API with retry logic.
        
        Args:
            prompt: Evaluation prompt
            model: Anthropic model name
            
        Returns:
            Parsed evaluation result
        """
        client = self._get_anthropic_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="Anthropic API key not configured. Please set ANTHROPIC_API_KEY environment variable."
            )
        
        # Map model name to Anthropic format
        model_map = {
            "claude-sonnet-4": "claude-sonnet-4-20250514",
            "claude-sonnet-3.5": "claude-3-5-sonnet-20241022"
        }
        anthropic_model = model_map.get(model, model)
        
        try:
            response = await client.messages.create(
                model=anthropic_model,
                max_tokens=2048,
                temperature=0.3,
                system=get_system_prompt(),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = response.content[0].text
            
            # Try to extract JSON from response
            result = self._extract_json(result)
            parsed = json.loads(result)
            
            return self._validate_and_normalize_result(parsed)
            
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse LLM response as JSON: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Anthropic API error: {str(e)}"
            )
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might contain markdown formatting."""
        # Remove markdown code blocks if present
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return text
    
    def _validate_and_normalize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize LLM response.
        
        Args:
            result: Raw LLM response
            
        Returns:
            Validated and normalized result
        """
        # Ensure required fields exist
        if "score" not in result:
            raise ValueError("LLM response missing 'score' field")
        if "reasoning" not in result:
            raise ValueError("LLM response missing 'reasoning' field")
        
        # Normalize score to 0-100 range
        score = float(result["score"])
        score = max(0, min(100, score))
        
        # Ensure issues is a list
        issues = result.get("issues", [])
        if not isinstance(issues, list):
            issues = []
        
        return {
            "score": score,
            "reasoning": str(result["reasoning"]),
            "issues": issues
        }


# Global judge instance
judge = LLMJudge()
