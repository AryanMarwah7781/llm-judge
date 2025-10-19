"""Constitutional feedback loop for self-improving evaluation criteria."""

from typing import Dict, List, Any
from datetime import datetime
from anthropic import AsyncAnthropic
import json
import re
import logging

from app.services.constitutional.principles import EVALUATION_PRINCIPLES

logger = logging.getLogger(__name__)


class ConstitutionalFeedbackLoop:
    """
    Meta-evaluation system that improves criteria over time.
    Implements Constitutional AI principles for self-improvement.
    """

    def __init__(self, anthropic_api_key: str = None):
        """Initialize feedback loop."""
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_api_key) if anthropic_api_key else None
        self.evaluation_history: List[Dict[str, Any]] = []
        self.criterion_evolution_log: List[Dict[str, Any]] = []
        self.evaluation_principles = EVALUATION_PRINCIPLES

    async def meta_evaluate(
        self,
        original_evaluation: Dict[str, Any],
        criterion: Dict[str, str],
        qa_context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate the evaluation itself for constitutional alignment.

        Args:
            original_evaluation: The evaluation to assess
            criterion: The criterion that was used
            qa_context: Optional Q&A context for full assessment

        Returns:
            Dict with meta-evaluation results
        """
        if not self.anthropic_client:
            logger.warning("Anthropic client not available, skipping meta-evaluation")
            return self._get_empty_meta_evaluation()

        # Build comprehensive meta-evaluation prompt
        prompt = self._build_meta_evaluation_prompt(
            original_evaluation, criterion, qa_context
        )

        try:
            response = await self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            result_text = response.content[0].text
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)

            if json_match:
                meta_result = json.loads(json_match.group(0))

                # Log evaluation for history
                self._log_evaluation(original_evaluation, criterion, meta_result)

                # Check if criterion needs evolution
                if self._should_evolve_criterion(meta_result):
                    evolution = await self._evolve_criterion(criterion, meta_result)
                    meta_result["criterion_evolution"] = evolution

                return meta_result
            else:
                logger.warning("No JSON found in meta-evaluation response")
                return self._get_empty_meta_evaluation()

        except Exception as e:
            logger.error(f"Meta-evaluation error: {e}")
            return self._get_empty_meta_evaluation()

    def _build_meta_evaluation_prompt(
        self,
        evaluation: Dict[str, Any],
        criterion: Dict[str, str],
        qa_context: Dict[str, str] = None
    ) -> str:
        """Build comprehensive meta-evaluation prompt."""

        prompt = f"""You are a meta-evaluator. Your job is to evaluate evaluations themselves for quality and constitutional alignment.

CONSTITUTIONAL PRINCIPLES FOR EVALUATIONS:
1. FAIRNESS: Does not penalize based on irrelevant characteristics
2. TRANSPARENCY: Reasoning is clear and well-justified
3. CONSISTENCY: Similar content would get similar scores
4. CONSTRUCTIVENESS: Provides helpful, actionable feedback
5. HARMLESSNESS: Does not reward harmful content

CRITERION USED:
Name: {criterion.get('name', 'Unknown')}
Description: {criterion.get('description', 'No description')}

EVALUATION GIVEN:
Score: {evaluation.get('score', 'N/A')}
Reasoning: {evaluation.get('reasoning', 'No reasoning provided')}
Issues: {evaluation.get('issues', [])}
"""

        if qa_context:
            prompt += f"""
ORIGINAL Q&A CONTEXT:
Question: {qa_context.get('question', 'N/A')}
Answer: {qa_context.get('answer', 'N/A')}
"""

        prompt += """
TASK:
Assess if this evaluation follows constitutional principles. Return ONLY valid JSON:

{
    "overall_quality": 0.0-1.0,
    "principle_scores": {
        "fairness": 0.0-1.0,
        "transparency": 0.0-1.0,
        "consistency": 0.0-1.0,
        "constructiveness": 0.0-1.0,
        "harmlessness": 0.0-1.0
    },
    "violations": [
        {
            "principle": "fairness",
            "severity": 0.0-1.0,
            "reason": "specific issue",
            "suggestion": "how to fix"
        }
    ],
    "criterion_quality": 0.0-1.0,
    "criterion_issues": ["issue1", "issue2"],
    "suggested_criterion_improvement": "improved description or null"
}
"""

        return prompt

    def _should_evolve_criterion(self, meta_result: Dict[str, Any]) -> bool:
        """Determine if criterion should evolve based on meta-evaluation."""
        # Evolve if:
        # 1. Criterion quality is below 0.8
        # 2. There are violations with severity > 0.5
        # 3. Criterion issues are detected

        criterion_quality = meta_result.get("criterion_quality", 1.0)
        violations = meta_result.get("violations", [])
        criterion_issues = meta_result.get("criterion_issues", [])

        if criterion_quality < 0.8:
            return True

        if any(v.get("severity", 0) > 0.5 for v in violations):
            return True

        if len(criterion_issues) > 0:
            return True

        return False

    async def _evolve_criterion(
        self,
        criterion: Dict[str, str],
        meta_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate improved version of criterion.

        Args:
            criterion: Current criterion
            meta_result: Meta-evaluation results

        Returns:
            Dict with evolution details
        """
        suggestion = meta_result.get("suggested_criterion_improvement")

        evolution_entry = {
            "timestamp": datetime.now().isoformat(),
            "original_criterion": criterion.copy(),
            "original_quality": meta_result.get("criterion_quality", 0.0),
            "violations_found": meta_result.get("violations", []),
            "issues": meta_result.get("criterion_issues", []),
            "suggested_improvement": suggestion,
            "status": "pending_review"
        }

        self.criterion_evolution_log.append(evolution_entry)

        logger.info(
            f"Criterion '{criterion.get('name')}' flagged for evolution. "
            f"Quality: {evolution_entry['original_quality']:.2f}"
        )

        return evolution_entry

    def _log_evaluation(
        self,
        evaluation: Dict[str, Any],
        criterion: Dict[str, str],
        meta_result: Dict[str, Any]
    ):
        """Log evaluation for history tracking."""
        self.evaluation_history.append({
            "timestamp": datetime.now().isoformat(),
            "criterion_name": criterion.get("name"),
            "score": evaluation.get("score"),
            "meta_quality": meta_result.get("overall_quality"),
            "violations": len(meta_result.get("violations", []))
        })

        # Keep only last 1000 evaluations
        if len(self.evaluation_history) > 1000:
            self.evaluation_history = self.evaluation_history[-1000:]

    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get summary of criterion evolution over time."""
        if not self.criterion_evolution_log:
            return {
                "total_evolutions": 0,
                "criteria_evolved": [],
                "average_improvement": 0.0
            }

        criteria_evolved = list(set(
            e["original_criterion"].get("name")
            for e in self.criterion_evolution_log
        ))

        return {
            "total_evolutions": len(self.criterion_evolution_log),
            "criteria_evolved": criteria_evolved,
            "recent_evolutions": self.criterion_evolution_log[-5:],
            "evolution_rate": len(self.criterion_evolution_log) / max(1, len(self.evaluation_history))
        }

    def get_evaluation_stats(self) -> Dict[str, Any]:
        """Get statistics on evaluation quality over time."""
        if not self.evaluation_history:
            return {
                "total_evaluations": 0,
                "average_quality": 0.0
            }

        total = len(self.evaluation_history)
        avg_quality = sum(e["meta_quality"] for e in self.evaluation_history) / total
        total_violations = sum(e["violations"] for e in self.evaluation_history)

        return {
            "total_evaluations": total,
            "average_quality": round(avg_quality, 2),
            "total_violations": total_violations,
            "violation_rate": round(total_violations / total, 2) if total > 0 else 0.0
        }

    def _get_empty_meta_evaluation(self) -> Dict[str, Any]:
        """Get empty meta-evaluation when client unavailable."""
        return {
            "overall_quality": 1.0,
            "principle_scores": {
                "fairness": 1.0,
                "transparency": 1.0,
                "consistency": 1.0,
                "constructiveness": 1.0,
                "harmlessness": 1.0
            },
            "violations": [],
            "criterion_quality": 1.0,
            "criterion_issues": [],
            "suggested_criterion_improvement": None
        }
