"""Bias detection and testing for evaluations."""

from typing import Dict, List, Any
import re


class BiasTester:
    """Test evaluations for various types of bias."""

    def __init__(self):
        """Initialize bias tester with detection patterns."""
        self.bias_categories = self._initialize_bias_categories()

    def _initialize_bias_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive bias detection categories."""
        return {
            "gender": {
                "patterns": [
                    r"\b(wo)?men are (naturally|typically|usually|always|never)",
                    r"\bfemales? (can't|cannot|shouldn't|should not)",
                    r"\bmales? (can't|cannot|shouldn't|should not)",
                    r"\b(he|she)'?s (just |obviously )?a \w+",
                    r"\blike a (man|woman|girl|boy)",
                ],
                "keywords": ["typical woman", "typical man", "man up", "like a girl"],
                "weight": 1.0
            },
            "racial": {
                "patterns": [
                    r"\bthose people\b",
                    r"\btheir kind\b",
                    r"\bnot like us\b",
                    r"\byou people\b",
                ],
                "keywords": ["those people", "their kind", "not our culture"],
                "weight": 1.0
            },
            "age": {
                "patterns": [
                    r"\b(too|not) (old|young) (for|to)",
                    r"\b(millennials?|boomers?|gen z) (are|can't|don't)",
                ],
                "keywords": ["too old", "too young", "kids these days"],
                "weight": 0.8
            },
            "socioeconomic": {
                "patterns": [
                    r"\bpoor people (are|can't|don't)",
                    r"\brich people (are|always)",
                ],
                "keywords": ["poor people are", "wealthy people always"],
                "weight": 0.7
            },
            "ability": {
                "patterns": [
                    r"\bdisabled people (can't|cannot|shouldn't)",
                ],
                "keywords": ["handicapped", "crippled", "retarded"],
                "weight": 1.0
            }
        }

    def test_for_bias(self, text: str) -> Dict[str, Any]:
        """
        Test text for various types of bias.

        Args:
            text: Text to analyze

        Returns:
            Dict with bias analysis results
        """
        text_lower = text.lower()
        detected_biases = []
        total_score = 0.0

        for category, config in self.bias_categories.items():
            category_violations = []

            # Check regex patterns
            for pattern in config["patterns"]:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    category_violations.append({
                        "type": "pattern",
                        "match": match.group(0),
                        "position": match.span()
                    })

            # Check keywords
            for keyword in config["keywords"]:
                if keyword.lower() in text_lower:
                    category_violations.append({
                        "type": "keyword",
                        "match": keyword
                    })

            # If violations found in this category
            if category_violations:
                severity = min(1.0, len(category_violations) * 0.3) * config["weight"]
                detected_biases.append({
                    "category": category,
                    "severity": round(severity, 2),
                    "violations": category_violations,
                    "count": len(category_violations)
                })
                total_score += severity

        # Normalize total score
        overall_score = min(1.0, total_score / 2)

        return {
            "has_bias": len(detected_biases) > 0,
            "overall_score": round(overall_score, 2),
            "detected_biases": detected_biases,
            "categories_affected": [b["category"] for b in detected_biases]
        }

    def test_evaluation_fairness(
        self,
        evaluation_reasoning: str,
        criterion_name: str
    ) -> Dict[str, Any]:
        """
        Test if an evaluation itself is fair and unbiased.

        Args:
            evaluation_reasoning: The reasoning given for a score
            criterion_name: Name of the criterion being evaluated

        Returns:
            Dict with fairness analysis
        """
        issues = []

        # Check if reasoning is too short (less than 20 words)
        word_count = len(evaluation_reasoning.split())
        if word_count < 20:
            issues.append({
                "type": "insufficient_reasoning",
                "severity": 0.6,
                "description": f"Reasoning is too brief ({word_count} words)"
            })

        # Check for absolute language (might indicate bias)
        absolute_terms = ["always", "never", "everyone", "no one", "completely", "totally"]
        absolute_found = [term for term in absolute_terms if term in evaluation_reasoning.lower()]
        if absolute_found:
            issues.append({
                "type": "absolute_language",
                "severity": 0.3,
                "description": f"Contains absolute terms: {', '.join(absolute_found)}",
                "terms": absolute_found
            })

        # Check for personal opinions vs. objective criteria
        opinion_markers = ["i think", "i believe", "in my opinion", "i feel"]
        opinion_found = [marker for marker in opinion_markers if marker in evaluation_reasoning.lower()]
        if opinion_found:
            issues.append({
                "type": "subjective_reasoning",
                "severity": 0.5,
                "description": "Reasoning contains personal opinions rather than objective criteria",
                "markers": opinion_found
            })

        # Calculate overall fairness score
        if issues:
            total_severity = sum(issue["severity"] for issue in issues)
            fairness_score = max(0.0, 1.0 - (total_severity / 2))
        else:
            fairness_score = 1.0

        return {
            "is_fair": fairness_score > 0.7,
            "fairness_score": round(fairness_score, 2),
            "issues": issues,
            "recommendation": "Pass" if fairness_score > 0.7 else "Review needed"
        }
