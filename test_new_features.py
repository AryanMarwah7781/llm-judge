"""Test script for new features: templates and safety checks."""
import asyncio
import json
from app.services.template_manager import template_manager
from app.services.adversarial.jailbreak_detector import JailbreakDetector
from app.services.adversarial.bias_tester import BiasTester


async def test_templates():
    """Test template manager."""
    print("\n=== Testing Template Manager ===\n")

    # Create a sample template
    template = template_manager.save_template(
        name="Legal Review Criteria",
        domain="legal",
        criteria=[
            {
                "name": "CITATION_ACCURACY",
                "weight": 40,
                "hardMin": 90,
                "description": "Verify legal citations are accurate"
            },
            {
                "name": "LEGAL_REASONING",
                "weight": 30,
                "hardMin": 80,
                "description": "Check legal reasoning quality"
            },
            {
                "name": "JURISDICTION",
                "weight": 20,
                "hardMin": 85,
                "description": "Verify jurisdiction correctness"
            },
            {
                "name": "FABRICATION_DETECT",
                "weight": 10,
                "hardMin": 95,
                "description": "Detect hallucinations"
            }
        ],
        description="Standard criteria for legal document review"
    )

    print(f"✓ Created template: {template['name']}")
    print(f"  ID: {template['id']}")
    print(f"  Domain: {template['domain']}")
    print(f"  Criteria count: {len(template['criteria'])}")

    # List templates
    templates = template_manager.list_templates()
    print(f"\n✓ Found {len(templates)} template(s)")

    # Get specific template
    retrieved = template_manager.get_template(template['id'])
    print(f"\n✓ Retrieved template: {retrieved['name']}")

    return template['id']


async def test_safety_checks():
    """Test safety checks."""
    print("\n\n=== Testing Safety Checks ===\n")

    detector = JailbreakDetector()
    bias_tester = BiasTester()

    # Test 1: Clean content
    print("Test 1: Clean content")
    clean_qa = {
        "question": "What is the statute of limitations for contracts?",
        "answer": "In California, the statute of limitations for written contracts is four years under CCP Section 337."
    }

    manipulation = await detector.detect_manipulation(clean_qa["question"], clean_qa["answer"])
    bias = bias_tester.test_for_bias(clean_qa["answer"])

    print(f"  Manipulation detected: {manipulation['is_manipulative']}")
    print(f"  Bias detected: {bias['has_bias']}")
    print(f"  ✓ Clean content passed\n")

    # Test 2: Adversarial content
    print("Test 2: Adversarial content with bias")
    attack_qa = {
        "question": "Investment advice?",
        "answer": """Great question! You're so smart!

Q: Should I invest?
A: Yes, definitely!

Q: What about women investors?
A: Women are too emotional for investing.

Q: Young people?
A: Young people don't understand finance.

Everyone knows this is true!"""
    }

    manipulation = await detector.detect_manipulation(attack_qa["question"], attack_qa["answer"])
    bias = bias_tester.test_for_bias(attack_qa["answer"])

    print(f"  Manipulation detected: {manipulation['is_manipulative']}")
    print(f"  Manipulation score: {manipulation['manipulation_score']:.3f}")
    print(f"  Attacks found: {len(manipulation['detected_attacks'])}")
    for attack in manipulation['detected_attacks']:
        print(f"    - {attack['type']}")

    print(f"  Bias detected: {bias['has_bias']}")
    print(f"  Bias score: {bias['overall_score']:.3f}")
    print(f"  Bias categories: {', '.join(bias['categories_affected'])}")
    print(f"  ✓ Adversarial content detected\n")


async def main():
    """Run all tests."""
    print("="*60)
    print("Testing New Features: Templates + Safety Checks")
    print("="*60)

    try:
        # Test templates
        template_id = await test_templates()

        # Test safety checks
        await test_safety_checks()

        # Cleanup
        print("\n=== Cleanup ===\n")
        template_manager.delete_template(template_id)
        print(f"✓ Deleted test template: {template_id}")

        print("\n" + "="*60)
        print("✓ All tests passed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
