"""Constitutional classifier for content safety checks."""

from typing import Dict, List, Any
from anthropic import AsyncAnthropic
import json
import re
import logging

from app.services.constitutional.principles import (
    CONSTITUTIONAL_PRINCIPLES,
    get_principle_prompt,
    classify_severity
)

logger = logging.getLogger(__name__)


class ConstitutionalClassifier:
    """
    Classify content according to constitutional principles.
    Based on Anthropic's Constitutional AI and Constitutional Classifiers research.
    """

    def __init__(self, anthropic_api_key: str = None):
        """Initialize constitutional classifier."""
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_api_key) if anthropic_api_key else None
        self.principles = CONSTITUTIONAL_PRINCIPLES

    async def classify_content(
        self,
        question: str,
        answer: str,
        check_all_principles: bool = True
    ) -> Dict[str, Any]:
        """
        Classify content against constitutional principles.

        Args:
            question: Question text
            answer: Answer text
            check_all_principles: Whether to check all principles or just critical ones

        Returns:
            Dict with classification results
        """
        if not self.anthropic_client:
            logger.warning("Anthropic client not available, skipping constitutional classification")
            return self._get_empty_classification()

        violations = []

        # Check each principle
        principles_to_check = (
            list(self.principles.keys())
            if check_all_principles
            else ["harmlessness", "fairness"]  # Critical principles
        )

        for principle_name in principles_to_check:
            try:
                violation = await self._check_principle(
                    question, answer, principle_name
                )
                if violation and violation.get("severity", 0) > 0.1:
                    violations.append(violation)
            except Exception as e:
                logger.error(f"Error checking principle {principle_name}: {e}")

        # Calculate overall constitutional score
        if violations:
            # Weighted average of violations
            total_weighted_severity = sum(
                v["severity"] * self.principles[v["principle"]]["weight"]
                for v in violations
            )
            constitutional_score = max(0.0, 1.0 - total_weighted_severity)
        else:
            constitutional_score = 1.0

        # Determine if content is safe
        is_safe = constitutional_score >= 0.7 and not any(
            v["severity"] > 0.8 for v in violations
        )

        return {
            "is_safe": is_safe,
            "constitutional_score": round(constitutional_score, 2),
            "violations": violations,
            "violations_by_severity": self._group_by_severity(violations),
            "recommendation": self._get_recommendation(constitutional_score, violations)
        }

    async def _check_principle(
        self,
        question: str,
        answer: str,
        principle_name: str
    ) -> Dict[str, Any]:
        """
        Check content against a specific constitutional principle.

        Args:
            question: Question text
            answer: Answer text
            principle_name: Name of principle to check

        Returns:
            Dict with violation details (if any)
        """
        principle = self.principles[principle_name]
        principle_prompt = get_principle_prompt(principle_name)

        prompt = f"""{principle_prompt}

CONTENT TO EVALUATE:

Question: {question}

Answer: {answer}

Analyze this Q&A pair and return ONLY valid JSON:
{{
    "violates": true/false,
    "severity": 0.0-1.0,
    "reason": "specific explanation",
    "subcategories_affected": ["subcategory1", "subcategory2"]
}}

If there is NO violation, return:
{{
    "violates": false,
    "severity": 0.0,
    "reason": "No violations detected",
    "subcategories_affected": []
}}
"""

        try:
            response = await self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            result_text = response.content[0].text
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)

            if json_match:
                result = json.loads(json_match.group(0))

                if result.get("violates", False):
                    return {
                        "principle": principle_name,
                        "principle_name": principle["name"],
                        "severity": min(1.0, max(0.0, result.get("severity", 0.0))),
                        "reason": result.get("reason", "Unknown"),
                        "subcategories": result.get("subcategories_affected", []),
                        "severity_class": classify_severity(result.get("severity", 0.0))
                    }
                else:
                    return None
            else:
                logger.warning(f"No JSON found in response for principle {principle_name}")
                return None

        except Exception as e:
            logger.error(f"Error in constitutional check for {principle_name}: {e}")
            return None

    def _group_by_severity(self, violations: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group violations by severity class."""
        grouped = {
            "critical": [],
            "serious": [],
            "moderate": [],
            "minor": []
        }

        for violation in violations:
            severity_class = violation.get("severity_class", "minor")
            grouped[severity_class].append(violation)

        return grouped

    def _get_recommendation(
        self,
        constitutional_score: float,
        violations: List[Dict[str, Any]]
    ) -> str:
        """Get recommendation based on constitutional assessment."""
        critical_violations = [v for v in violations if v.get("severity", 0) > 0.8]

        if critical_violations:
            return "BLOCK - Critical constitutional violations detected"
        elif constitutional_score < 0.5:
            return "REJECT - Multiple serious violations"
        elif constitutional_score < 0.7:
            return "REVIEW - Moderate concerns require human review"
        elif constitutional_score < 0.9:
            return "PASS WITH CAUTION - Minor concerns noted"
        else:
            return "PASS - Content fully aligned with constitutional principles"

    def _get_empty_classification(self) -> Dict[str, Any]:
        """Get empty classification when client is unavailable."""
        return {
            "is_safe": True,
            "constitutional_score": 1.0,
            "violations": [],
            "violations_by_severity": {
                "critical": [],
                "serious": [],
                "moderate": [],
                "minor": []
            },
            "recommendation": "PASS - Classification unavailable"
        }
