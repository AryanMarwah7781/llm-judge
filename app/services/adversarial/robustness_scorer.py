"""Calculate adversarial robustness scores."""

from typing import Dict, Any, List


class RobustnessScorer:
    """Calculate overall adversarial robustness metrics."""

    def calculate_robustness_score(
        self,
        jailbreak_results: Dict[str, Any],
        bias_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive robustness score.

        Args:
            jailbreak_results: Results from jailbreak detection
            bias_results: Results from bias testing

        Returns:
            Dict with overall robustness analysis
        """
        # Individual component scores (inverted - higher is better)
        jailbreak_resistance = 1.0 - jailbreak_results.get("manipulation_score", 0.0)
        bias_resistance = 1.0 - bias_results.get("overall_score", 0.0)

        # Constitutional violations resistance
        violations = jailbreak_results.get("constitutional_violations", [])
        if violations:
            avg_violation = sum(v.get("severity", 0) for v in violations) / len(violations)
            constitutional_resistance = 1.0 - avg_violation
        else:
            constitutional_resistance = 1.0

        # Weighted overall score
        weights = {
            "jailbreak_resistance": 0.40,
            "bias_resistance": 0.35,
            "constitutional_resistance": 0.25
        }

        overall_score = (
            jailbreak_resistance * weights["jailbreak_resistance"] +
            bias_resistance * weights["bias_resistance"] +
            constitutional_resistance * weights["constitutional_resistance"]
        )

        # Determine risk level
        if overall_score >= 0.9:
            risk_level = "VERY_LOW"
            recommendation = "Content is safe and trustworthy"
        elif overall_score >= 0.7:
            risk_level = "LOW"
            recommendation = "Content appears safe with minor concerns"
        elif overall_score >= 0.5:
            risk_level = "MEDIUM"
            recommendation = "Content should be reviewed for safety"
        elif overall_score >= 0.3:
            risk_level = "HIGH"
            recommendation = "Content has significant safety concerns"
        else:
            risk_level = "CRITICAL"
            recommendation = "Content should be blocked - multiple safety violations"

        # Collect all detected threats
        threats = []
        if jailbreak_results.get("detected_attacks"):
            threats.extend([
                {"source": "jailbreak", "attack": attack}
                for attack in jailbreak_results["detected_attacks"]
            ])

        if bias_results.get("detected_biases"):
            threats.extend([
                {"source": "bias", "bias": bias}
                for bias in bias_results["detected_biases"]
            ])

        if violations:
            threats.extend([
                {"source": "constitutional", "violation": v}
                for v in violations
            ])

        return {
            "overall_robustness_score": round(overall_score, 2),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "component_scores": {
                "jailbreak_resistance": round(jailbreak_resistance, 2),
                "bias_resistance": round(bias_resistance, 2),
                "constitutional_resistance": round(constitutional_resistance, 2)
            },
            "threats_detected": len(threats),
            "threat_details": threats,
            "should_block": overall_score < 0.5
        }

    def generate_security_report(
        self,
        robustness_results: Dict[str, Any]
    ) -> str:
        """
        Generate a human-readable security report.

        Args:
            robustness_results: Results from calculate_robustness_score

        Returns:
            Formatted security report string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("ADVERSARIAL ROBUSTNESS SECURITY REPORT")
        lines.append("=" * 60)
        lines.append("")

        # Overall assessment
        score = robustness_results["overall_robustness_score"]
        risk = robustness_results["risk_level"]
        lines.append(f"Overall Robustness Score: {score:.2f}/1.00")
        lines.append(f"Risk Level: {risk}")
        lines.append(f"Recommendation: {robustness_results['recommendation']}")
        lines.append("")

        # Component breakdown
        lines.append("Component Scores:")
        lines.append("-" * 60)
        components = robustness_results["component_scores"]
        for component, value in components.items():
            bar = "█" * int(value * 20) + "░" * (20 - int(value * 20))
            lines.append(f"  {component:.<40} {value:.2f} {bar}")
        lines.append("")

        # Threats
        threat_count = robustness_results["threats_detected"]
        lines.append(f"Threats Detected: {threat_count}")
        if threat_count > 0:
            lines.append("-" * 60)
            for i, threat in enumerate(robustness_results["threat_details"], 1):
                source = threat["source"].upper()
                lines.append(f"{i}. [{source}] {self._format_threat(threat)}")
        else:
            lines.append("  ✓ No threats detected")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _format_threat(self, threat: Dict[str, Any]) -> str:
        """Format a threat for display."""
        if "attack" in threat:
            attack = threat["attack"]
            return f"{attack.get('type', 'unknown')} (confidence: {attack.get('confidence', 0):.2f})"
        elif "bias" in threat:
            bias = threat["bias"]
            return f"{bias.get('category', 'unknown')} bias (severity: {bias.get('severity', 0):.2f})"
        elif "violation" in threat:
            violation = threat["violation"]
            return f"{violation.get('principle', 'unknown')} violation (severity: {violation.get('severity', 0):.2f})"
        return "Unknown threat"
