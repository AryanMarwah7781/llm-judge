"""Criteria validation and processing service."""
from typing import List, Dict, Any
from fastapi import HTTPException

from app.models.schemas import Criterion


class CriteriaValidator:
    """Service for validating and processing evaluation criteria."""
    
    @staticmethod
    def validate_criteria(criteria: List[Criterion]) -> None:
        """
        Validate criteria list.
        
        Args:
            criteria: List of criteria to validate
            
        Raises:
            HTTPException: If validation fails
        """
        if not criteria:
            raise HTTPException(
                status_code=400,
                detail="At least one criterion is required"
            )
        
        # Check for duplicate names
        names = [c.name for c in criteria]
        if len(names) != len(set(names)):
            raise HTTPException(
                status_code=400,
                detail="Duplicate criterion names found"
            )
        
        # Validate weights sum to 100
        total_weight = sum(c.weight for c in criteria)
        if abs(total_weight - 100) > 0.01:
            raise HTTPException(
                status_code=400,
                detail=f"Criteria weights must sum to 100, got {total_weight:.2f}"
            )
        
        # Validate each criterion
        for criterion in criteria:
            if not criterion.name or not criterion.name.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Criterion name cannot be empty"
                )
            
            if criterion.weight <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Criterion '{criterion.name}' has invalid weight: {criterion.weight}"
                )
            
            if criterion.hardMin < 0 or criterion.hardMin > 100:
                raise HTTPException(
                    status_code=400,
                    detail=f"Criterion '{criterion.name}' has invalid hardMin: {criterion.hardMin}"
                )
    
    @staticmethod
    def calculate_weighted_score(
        scores: Dict[str, float],
        criteria: List[Criterion]
    ) -> float:
        """
        Calculate weighted average score.
        
        Args:
            scores: Dict of criterion name to score
            criteria: List of criteria with weights
            
        Returns:
            Weighted average score
        """
        weighted_sum = 0.0
        total_weight = 0.0
        
        for criterion in criteria:
            if criterion.name in scores:
                weighted_sum += scores[criterion.name] * criterion.weight
                total_weight += criterion.weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    @staticmethod
    def check_hard_minimums(
        scores: Dict[str, float],
        criteria: List[Criterion]
    ) -> tuple[bool, List[str]]:
        """
        Check if all hard minimums are met.
        
        Args:
            scores: Dict of criterion name to score
            criteria: List of criteria with hard minimums
            
        Returns:
            Tuple of (all_passed, list_of_failed_criteria)
        """
        failed_criteria = []
        
        for criterion in criteria:
            if criterion.name in scores:
                if scores[criterion.name] < criterion.hardMin:
                    failed_criteria.append(criterion.name)
        
        return len(failed_criteria) == 0, failed_criteria
    
    @staticmethod
    def get_criterion_map(criteria: List[Criterion]) -> Dict[str, Criterion]:
        """
        Create a map of criterion name to criterion object.
        
        Args:
            criteria: List of criteria
            
        Returns:
            Dict mapping criterion name to criterion
        """
        return {c.name: c for c in criteria}


# Global validator instance
criteria_validator = CriteriaValidator()
