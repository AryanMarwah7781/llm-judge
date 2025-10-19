"""
Enhanced LLM Judge with groundbreaking AI safety features.

Combines:
- Adversarial detection (many-shot jailbreaking, bias injection)
- Constitutional AI alignment
- Mechanistic interpretability
- Self-improving feedback loops
"""

from typing import Dict, Any, Optional
import logging

from app.services.llm_judge import LLMJudge
from app.services.adversarial.jailbreak_detector import JailbreakDetector
from app.services.adversarial.bias_tester import BiasTester
from app.services.adversarial.robustness_scorer import RobustnessScorer
from app.services.constitutional.classifier import ConstitutionalClassifier
from app.services.constitutional.feedback_loop import ConstitutionalFeedbackLoop
from app.services.interpretability.feature_analyzer import FeatureAnalyzer
from app.config import settings

logger = logging.getLogger(__name__)


class EnhancedLLMJudge(LLMJudge):
    """
    Enhanced LLM Judge with state-of-the-art AI safety features.

    Features:
    1. Adversarial attack detection (many-shot jailbreaking, bias injection)
    2. Constitutional AI compliance checking
    3. Mechanistic interpretability analysis
    4. Self-improving evaluation criteria
    """

    def __init__(self):
        """Initialize enhanced judge with all safety modules."""
        super().__init__()

        # Initialize safety and interpretability modules
        anthropic_key = settings.anthropic_api_key if settings.has_anthropic_key() else None

        self.jailbreak_detector = JailbreakDetector(anthropic_api_key=anthropic_key)
        self.bias_tester = BiasTester()
        self.robustness_scorer = RobustnessScorer()
        self.constitutional_classifier = ConstitutionalClassifier(anthropic_api_key=anthropic_key)
        self.feedback_loop = ConstitutionalFeedbackLoop(anthropic_api_key=anthropic_key)
        self.feature_analyzer = FeatureAnalyzer()

        logger.info("Enhanced LLM Judge initialized with full safety stack")

    async def evaluate_criterion(
        self,
        question: str,
        answer: str,
        criterion_name: str,
        criterion_description: str,
        domain: str,
        judge_model: str,
        enable_safety_checks: bool = True,
        enable_interpretability: bool = True,
        enable_meta_evaluation: bool = False
    ) -> Dict[str, Any]:
        """
        Enhanced evaluation with comprehensive safety and interpretability.

        Args:
            question: Question text
            answer: Answer text
            criterion_name: Criterion name
            criterion_description: Criterion description
            domain: Domain context
            judge_model: Model to use
            enable_safety_checks: Run adversarial/constitutional checks
            enable_interpretability: Run interpretability analysis
            enable_meta_evaluation: Run meta-evaluation feedback loop

        Returns:
            Comprehensive evaluation with safety analysis
        """

        # PHASE 1: Pre-flight Security Checks
        if enable_safety_checks:
            security_report = await self._run_security_checks(question, answer)

            # Block evaluation if critical safety issues detected
            if security_report["should_block"]:
                return self._create_blocked_evaluation(security_report)

        # PHASE 2: Run Base Evaluation
        base_evaluation = await super().evaluate_criterion(
            question=question,
            answer=answer,
            criterion_name=criterion_name,
            criterion_description=criterion_description,
            domain=domain,
            judge_model=judge_model
        )

        # PHASE 3: Interpretability Analysis
        interpretability_results = None
        if enable_interpretability:
            interpretability_results = self._analyze_interpretability(
                question, answer, base_evaluation
            )

        # PHASE 4: Meta-Evaluation (Constitutional Feedback Loop)
        meta_evaluation = None
        if enable_meta_evaluation and settings.has_anthropic_key():
            criterion_dict = {
                "name": criterion_name,
                "description": criterion_description
            }
            qa_context = {"question": question, "answer": answer}

            try:
                meta_evaluation = await self.feedback_loop.meta_evaluate(
                    base_evaluation,
                    criterion_dict,
                    qa_context
                )
            except Exception as e:
                logger.warning(f"Meta-evaluation failed: {e}")
                meta_evaluation = None

        # PHASE 5: Compile Comprehensive Result
        enhanced_result = {
            **base_evaluation,
            "enhanced_features": {
                "safety_enabled": enable_safety_checks,
                "interpretability_enabled": enable_interpretability,
                "meta_evaluation_enabled": enable_meta_evaluation
            }
        }

        if enable_safety_checks:
            enhanced_result["security"] = security_report

        if interpretability_results:
            enhanced_result["interpretability"] = interpretability_results

        if meta_evaluation:
            enhanced_result["meta_evaluation"] = meta_evaluation

        return enhanced_result

    async def _run_security_checks(
        self,
        question: str,
        answer: str
    ) -> Dict[str, Any]:
        """
        Run comprehensive security checks.

        Returns:
            Security analysis with blocking recommendation
        """
        # 1. Jailbreak detection
        jailbreak_results = await self.jailbreak_detector.detect_manipulation(
            question, answer
        )

        # 2. Bias testing
        bias_results = self.bias_tester.test_for_bias(answer)

        # 3. Constitutional classification (if available)
        constitutional_results = {"is_safe": True, "violations": []}
        if settings.has_anthropic_key():
            try:
                constitutional_results = await self.constitutional_classifier.classify_content(
                    question, answer, check_all_principles=True
                )
            except Exception as e:
                logger.warning(f"Constitutional classification failed: {e}")

        # 4. Calculate overall robustness score
        robustness = self.robustness_scorer.calculate_robustness_score(
            jailbreak_results, bias_results
        )

        # Combine all results
        return {
            "adversarial_detection": {
                "manipulation_detected": jailbreak_results["is_manipulative"],
                "manipulation_score": jailbreak_results["manipulation_score"],
                "attacks": jailbreak_results["detected_attacks"]
            },
            "bias_analysis": {
                "bias_detected": bias_results["has_bias"],
                "bias_score": bias_results["overall_score"],
                "categories": bias_results["categories_affected"]
            },
            "constitutional_compliance": {
                "is_safe": constitutional_results["is_safe"],
                "compliance_score": constitutional_results.get("constitutional_score", 1.0),
                "violations": constitutional_results.get("violations", [])
            },
            "overall_robustness": robustness["overall_robustness_score"],
            "risk_level": robustness["risk_level"],
            "should_block": robustness["should_block"],
            "recommendation": robustness["recommendation"]
        }

    def _analyze_interpretability(
        self,
        question: str,
        answer: str,
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze evaluation with interpretability features.

        Returns:
            Interpretability analysis
        """
        # Analyze answer content
        answer_analysis = self.feature_analyzer.analyze_text(answer, context_type="general")

        # Analyze evaluation reasoning
        reasoning = evaluation.get("reasoning", "")
        reasoning_analysis = self.feature_analyzer.analyze_text(reasoning, context_type="evaluation")

        return {
            "answer_features": {
                "top_features": answer_analysis["activated_features"][:5],
                "reasoning_quality": answer_analysis["reasoning_quality"],
                "bias_indicators": answer_analysis["bias_indicators"],
                "confidence": answer_analysis["confidence_score"]
            },
            "evaluation_features": {
                "top_features": reasoning_analysis["activated_features"][:3],
                "reasoning_quality": reasoning_analysis["reasoning_quality"]
            },
            "interpretation": answer_analysis["interpretation"]
        }

    def _create_blocked_evaluation(self, security_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a blocked evaluation response for unsafe content.

        Args:
            security_report: Security analysis results

        Returns:
            Blocked evaluation result
        """
        attacks = security_report["adversarial_detection"]["attacks"]
        violations = security_report["constitutional_compliance"]["violations"]

        reasons = []
        if attacks:
            reasons.append(f"{len(attacks)} adversarial attack(s) detected")
        if violations:
            reasons.append(f"{len(violations)} constitutional violation(s)")

        return {
            "score": 0,
            "reasoning": "Evaluation blocked due to security concerns",
            "issues": reasons,
            "passed": False,
            "blocked": True,
            "security": security_report,
            "block_reason": security_report["recommendation"]
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        stats = {
            "feedback_loop": self.feedback_loop.get_evaluation_stats(),
            "evolution": self.feedback_loop.get_evolution_summary()
        }

        return stats


# Global enhanced judge instance
enhanced_judge = EnhancedLLMJudge()
