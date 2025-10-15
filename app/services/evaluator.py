"""Core evaluation orchestration service."""
import asyncio
from typing import List, Dict
from fastapi import HTTPException

from app.models.schemas import (
    QAPair,
    Criterion,
    QAEvaluation,
    CriterionScore,
    EvaluationResponse,
    EvaluationSummary
)
from app.services.llm_judge import judge
from app.services.criteria import criteria_validator


class EvaluationService:
    """Service for orchestrating Q&A evaluations."""
    
    async def evaluate_qa_pairs(
        self,
        qa_pairs: List[QAPair],
        criteria: List[Criterion],
        judge_model: str,
        global_threshold: float,
        domain: str
    ) -> EvaluationResponse:
        """
        Evaluate all Q&A pairs against criteria.
        
        Args:
            qa_pairs: List of Q&A pairs to evaluate
            criteria: Evaluation criteria
            judge_model: LLM judge model to use
            global_threshold: Global pass/fail threshold
            domain: Domain context
            
        Returns:
            Complete evaluation results
        """
        # Validate criteria
        criteria_validator.validate_criteria(criteria)
        
        # Evaluate all Q&A pairs concurrently
        evaluation_tasks = [
            self._evaluate_single_qa(
                qa_pair=qa_pair,
                criteria=criteria,
                judge_model=judge_model,
                global_threshold=global_threshold,
                domain=domain
            )
            for qa_pair in qa_pairs
        ]
        
        evaluations = await asyncio.gather(*evaluation_tasks, return_exceptions=True)
        
        # Handle any errors
        processed_evaluations = []
        for idx, result in enumerate(evaluations):
            if isinstance(result, Exception):
                # Create failed evaluation for this Q&A
                qa_pair = qa_pairs[idx]
                processed_evaluations.append(
                    self._create_failed_evaluation(qa_pair, str(result))
                )
            else:
                processed_evaluations.append(result)
        
        # Calculate summary
        summary = self._calculate_summary(processed_evaluations)
        
        return EvaluationResponse(
            evaluations=processed_evaluations,
            summary=summary
        )
    
    async def _evaluate_single_qa(
        self,
        qa_pair: QAPair,
        criteria: List[Criterion],
        judge_model: str,
        global_threshold: float,
        domain: str
    ) -> QAEvaluation:
        """
        Evaluate a single Q&A pair.
        
        Args:
            qa_pair: Q&A pair to evaluate
            criteria: Evaluation criteria
            judge_model: LLM judge model
            global_threshold: Global pass/fail threshold
            domain: Domain context
            
        Returns:
            Evaluation result for this Q&A pair
        """
        # Evaluate each criterion concurrently
        criterion_tasks = [
            judge.evaluate_criterion(
                question=qa_pair.question,
                answer=qa_pair.answer,
                criterion_name=criterion.name,
                criterion_description=criterion.description,
                domain=domain,
                judge_model=judge_model
            )
            for criterion in criteria
        ]
        
        criterion_results = await asyncio.gather(*criterion_tasks)
        
        # Build scores dictionary
        scores: Dict[str, CriterionScore] = {}
        raw_scores: Dict[str, float] = {}
        
        for criterion, result in zip(criteria, criterion_results):
            score_value = result["score"]
            passed_hard_min = score_value >= criterion.hardMin
            
            scores[criterion.name] = CriterionScore(
                score=score_value,
                reasoning=result["reasoning"],
                passed=passed_hard_min,
                issues=result.get("issues", [])
            )
            raw_scores[criterion.name] = score_value
        
        # Calculate weighted score
        weighted_score = criteria_validator.calculate_weighted_score(
            raw_scores, criteria
        )
        
        # Check hard minimums
        hard_mins_passed, failed_criteria = criteria_validator.check_hard_minimums(
            raw_scores, criteria
        )
        
        # Determine verdict
        verdict = "PASS"
        reason = None
        
        if not hard_mins_passed:
            verdict = "REJECT"
            reason = f"Failed hard minimum on: {', '.join(failed_criteria)}"
        elif weighted_score < global_threshold:
            verdict = "REJECT"
            reason = f"Weighted score {weighted_score:.1f} below threshold {global_threshold}"
        
        return QAEvaluation(
            qa_id=qa_pair.qa_id,
            question=qa_pair.question,
            answer=qa_pair.answer,
            scores=scores,
            weighted_score=round(weighted_score, 2),
            verdict=verdict,
            reason=reason
        )
    
    def _create_failed_evaluation(
        self,
        qa_pair: QAPair,
        error_message: str
    ) -> QAEvaluation:
        """
        Create a failed evaluation result for error cases.
        
        Args:
            qa_pair: The Q&A pair that failed
            error_message: Error message
            
        Returns:
            Failed evaluation result
        """
        return QAEvaluation(
            qa_id=qa_pair.qa_id,
            question=qa_pair.question,
            answer=qa_pair.answer,
            scores={},
            weighted_score=0.0,
            verdict="REJECT",
            reason=f"Evaluation failed: {error_message}"
        )
    
    def _calculate_summary(
        self,
        evaluations: List[QAEvaluation]
    ) -> EvaluationSummary:
        """
        Calculate summary statistics.
        
        Args:
            evaluations: List of evaluation results
            
        Returns:
            Summary statistics
        """
        total = len(evaluations)
        passed = sum(1 for e in evaluations if e.verdict == "PASS")
        failed = total - passed
        
        avg_score = 0.0
        if total > 0:
            avg_score = sum(e.weighted_score for e in evaluations) / total
        
        return EvaluationSummary(
            total=total,
            passed=passed,
            failed=failed,
            avg_score=round(avg_score, 2)
        )


# Global evaluator instance
evaluator = EvaluationService()
