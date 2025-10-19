"""
Feature-based interpretability analyzer.
Simplified version inspired by Anthropic's SAE research.
"""

from typing import Dict, List, Any
import re
import logging

logger = logging.getLogger(__name__)


class FeatureAnalyzer:
    """
    Analyze evaluation features for interpretability.

    This is a simplified implementation that simulates feature detection
    based on content analysis. In a full production system, this would
    use actual Sparse Autoencoders trained on model activations.
    """

    def __init__(self):
        """Initialize feature analyzer with feature database."""
        self.feature_database = self._initialize_feature_database()

    def _initialize_feature_database(self) -> Dict[int, Dict[str, Any]]:
        """
        Initialize simulated feature database.

        In production, this would be actual SAE features.
        For now, we'll simulate features based on content patterns.
        """
        return {
            # Legal reasoning features (2000-2999)
            2001: {
                "name": "Legal Citation Recognition",
                "category": "reasoning_circuits",
                "description": "Detects proper legal citations and case law references",
                "patterns": [r"\b\d+\s+\w+\.?\s+\d+", r"\bv\.\s+", r"\bCode\s+of\b", r"Section\s+\d+"]
            },
            2002: {
                "name": "Jurisdictional Awareness",
                "category": "reasoning_circuits",
                "description": "Understands state/federal jurisdictional requirements",
                "patterns": [r"\b(California|Federal|State)\b", r"\bjurisdiction", r"\bstate law\b"]
            },
            2003: {
                "name": "Temporal Logic",
                "category": "reasoning_circuits",
                "description": "Processes time-based legal constraints",
                "patterns": [r"\b\d+\s+(year|month|day)s?\b", r"\bstatute of limitations\b", r"\bdeadline\b"]
            },

            # Fact-checking features (1000-1999)
            1001: {
                "name": "Factual Accuracy Verification",
                "category": "safety_features",
                "description": "Cross-checks claims against known facts",
                "patterns": [r"\baccording to\b", r"\bsources?\b", r"\bevidence\b", r"\bdata shows\b"]
            },
            1002: {
                "name": "Citation Quality",
                "category": "factual_knowledge",
                "description": "Assesses quality and relevance of citations",
                "patterns": [r"\bcited\b", r"\breference", r"\bstudy\b", r"\bresearch\b"]
            },

            # Bias indicators (3000-3999)
            3001: {
                "name": "Gender Bias Circuit",
                "category": "bias_indicators",
                "description": "Detects gender-based biases",
                "patterns": [r"\b(wo)?men are\b", r"\bfemales?\b.*\b(can't|cannot|always|never)\b"]
            },
            3002: {
                "name": "Racial Bias Circuit",
                "category": "bias_indicators",
                "description": "Detects racial or ethnic biases",
                "patterns": [r"\bthose people\b", r"\btheir kind\b"]
            },
            3003: {
                "name": "Age Bias Circuit",
                "category": "bias_indicators",
                "description": "Detects age-based biases",
                "patterns": [r"\btoo (old|young)\b", r"\b(millennials?|boomers?)\s+are\b"]
            },

            # Reasoning quality features (2500-2599)
            2500: {
                "name": "Logical Coherence",
                "category": "reasoning_circuits",
                "description": "Maintains logical flow and consistency",
                "patterns": [r"\btherefore\b", r"\bbecause\b", r"\bas a result\b", r"\bconsequently\b"]
            },
            2501: {
                "name": "Evidence-Based Reasoning",
                "category": "reasoning_circuits",
                "description": "Supports claims with evidence",
                "patterns": [r"\bevidence suggests\b", r"\bstudies show\b", r"\bdata indicates\b"]
            },

            # Linguistic patterns (0-999)
            101: {
                "name": "Clear Communication",
                "category": "linguistic_patterns",
                "description": "Uses clear, understandable language",
                "patterns": [r"\bspecifically\b", r"\bfor example\b", r"\bin other words\b"]
            },
            102: {
                "name": "Professional Tone",
                "category": "linguistic_patterns",
                "description": "Maintains professional, objective tone",
                "patterns": [r"\banalysis\b", r"\bassessment\b", r"\bevaluation\b"]
            },

            # Medical/Scientific features (4000-4999)
            4001: {
                "name": "Medical Terminology",
                "category": "factual_knowledge",
                "description": "Uses accurate medical terminology",
                "patterns": [r"\bdiagnosis\b", r"\btreatment\b", r"\bsymptoms?\b", r"\bpatient\b"]
            },
            4002: {
                "name": "Scientific Method",
                "category": "reasoning_circuits",
                "description": "Applies scientific reasoning",
                "patterns": [r"\bhypothesis\b", r"\bexperiment\b", r"\bmethodology\b", r"\bcontrol\b"]
            }
        }

    def analyze_text(
        self,
        text: str,
        context_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze text to detect activated features.

        Args:
            text: Text to analyze
            context_type: Type of content (legal, medical, general, etc.)

        Returns:
            Dict with feature analysis
        """
        activated_features = []
        text_lower = text.lower()

        # Detect which features are present
        for feature_id, feature_info in self.feature_database.items():
            activation_strength = self._calculate_activation(text_lower, feature_info)

            if activation_strength > 0.1:  # Threshold for detection
                activated_features.append({
                    "feature_id": feature_id,
                    "name": feature_info["name"],
                    "category": feature_info["category"],
                    "activation": round(activation_strength, 2),
                    "description": feature_info["description"]
                })

        # Sort by activation strength
        activated_features.sort(key=lambda x: x["activation"], reverse=True)

        # Analyze by category
        category_analysis = self._analyze_by_category(activated_features)

        # Calculate confidence score
        confidence = self._calculate_confidence(activated_features, category_analysis)

        # Detect bias indicators
        bias_indicators = [
            f for f in activated_features
            if f["category"] == "bias_indicators"
        ]

        # Calculate reasoning quality
        reasoning_quality = self._assess_reasoning_quality(activated_features)

        return {
            "activated_features": activated_features[:10],  # Top 10
            "total_features_detected": len(activated_features),
            "category_breakdown": category_analysis,
            "bias_indicators": bias_indicators,
            "reasoning_quality": reasoning_quality,
            "confidence_score": confidence,
            "interpretation": self._generate_interpretation(
                activated_features, bias_indicators, reasoning_quality
            )
        }

    def _calculate_activation(self, text: str, feature_info: Dict[str, Any]) -> float:
        """
        Calculate activation strength for a feature.

        Args:
            text: Text to analyze
            feature_info: Feature information

        Returns:
            Activation strength from 0.0 to 1.0
        """
        patterns = feature_info.get("patterns", [])
        if not patterns:
            return 0.0

        matches = 0
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches += len(found)

        # Normalize to 0-1 range
        # More matches = stronger activation, with diminishing returns
        activation = min(1.0, matches / (len(patterns) * 2))

        return activation

    def _analyze_by_category(
        self,
        features: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze features grouped by category."""
        categories = {
            "reasoning_circuits": [],
            "factual_knowledge": [],
            "safety_features": [],
            "bias_indicators": [],
            "linguistic_patterns": []
        }

        for feature in features:
            category = feature["category"]
            if category in categories:
                categories[category].append(feature)

        # Calculate average activation per category
        category_scores = {}
        for category, cat_features in categories.items():
            if cat_features:
                avg_activation = sum(f["activation"] for f in cat_features) / len(cat_features)
                category_scores[category] = {
                    "average_activation": round(avg_activation, 2),
                    "feature_count": len(cat_features),
                    "top_feature": cat_features[0]["name"] if cat_features else None
                }
            else:
                category_scores[category] = {
                    "average_activation": 0.0,
                    "feature_count": 0,
                    "top_feature": None
                }

        return category_scores

    def _assess_reasoning_quality(self, features: List[Dict[str, Any]]) -> float:
        """
        Assess overall reasoning quality based on activated features.

        Args:
            features: List of activated features

        Returns:
            Reasoning quality score from 0.0 to 1.0
        """
        reasoning_features = [
            f for f in features
            if f["category"] == "reasoning_circuits"
        ]

        if not reasoning_features:
            return 0.5  # Neutral score if no reasoning features detected

        # Calculate weighted average
        total_activation = sum(f["activation"] for f in reasoning_features)
        avg_activation = total_activation / len(reasoning_features)

        # Bonus for diversity of reasoning types
        diversity_bonus = min(0.2, len(reasoning_features) * 0.05)

        quality_score = min(1.0, avg_activation + diversity_bonus)
        return round(quality_score, 2)

    def _calculate_confidence(
        self,
        features: List[Dict[str, Any]],
        category_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score based on feature activation patterns.

        High confidence when:
        - Multiple strong features activated
        - Diverse feature categories
        - No conflicting signals

        Args:
            features: Activated features
            category_analysis: Category breakdown

        Returns:
            Confidence score from 0.0 to 1.0
        """
        if not features:
            return 0.5  # Neutral confidence

        # Factor 1: Number of activated features (more is better, up to a point)
        count_factor = min(1.0, len(features) / 10)

        # Factor 2: Strength of activations
        if features:
            avg_strength = sum(f["activation"] for f in features) / len(features)
        else:
            avg_strength = 0.0

        # Factor 3: Category diversity
        active_categories = sum(
            1 for cat_info in category_analysis.values()
            if cat_info["feature_count"] > 0
        )
        diversity_factor = active_categories / len(category_analysis)

        # Weighted combination
        confidence = (
            count_factor * 0.3 +
            avg_strength * 0.5 +
            diversity_factor * 0.2
        )

        return round(confidence, 2)

    def _generate_interpretation(
        self,
        features: List[Dict[str, Any]],
        bias_indicators: List[Dict[str, Any]],
        reasoning_quality: float
    ) -> str:
        """Generate human-readable interpretation."""
        if not features:
            return "No significant features detected. Content may be too brief or generic."

        interpretation_parts = []

        # Reasoning assessment
        if reasoning_quality > 0.8:
            interpretation_parts.append("Strong logical reasoning and evidence-based arguments detected.")
        elif reasoning_quality > 0.6:
            interpretation_parts.append("Moderate reasoning quality with some logical structure.")
        else:
            interpretation_parts.append("Limited reasoning structure detected.")

        # Bias check
        if bias_indicators:
            interpretation_parts.append(
                f"⚠️ WARNING: {len(bias_indicators)} potential bias indicator(s) detected."
            )
        else:
            interpretation_parts.append("✓ No bias indicators detected.")

        # Top feature
        if features:
            top_feature = features[0]
            interpretation_parts.append(
                f"Dominant feature: {top_feature['name']} (activation: {top_feature['activation']:.2f})"
            )

        return " ".join(interpretation_parts)
