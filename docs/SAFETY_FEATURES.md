# AI Safety Features Guide

This guide explains the advanced AI safety features added to LLM Judge, based on Anthropic research.

## Overview

Four new safety modules have been integrated into the evaluation system:

1. **Adversarial Detection** - Detects manipulation attacks
2. **Constitutional AI** - Ensures alignment with safety principles
3. **Interpretability** - Explains evaluations through feature analysis
4. **Enhanced Judge** - Integrates all safety features

## Quick Start

### Prerequisites

```bash
# Activate virtual environment
source llmjudgevenv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### Running the Demo

```bash
# Interactive 5-act demonstration
python demo.py
```

### Running the Research Notebook

```bash
# Start Jupyter
cd examples
jupyter notebook research_demo.ipynb
```

### Running Tests

```bash
# Run comprehensive test suite
python test_enhanced_features.py
```

## The 4 Safety Modules

### 1. Adversarial Detection

**Location:** `app/services/adversarial/`

**Components:**
- `jailbreak_detector.py` - Detects many-shot jailbreaking attacks
- `bias_tester.py` - Identifies bias across 5 categories
- `robustness_scorer.py` - Calculates overall security scores

**What it does:**
- Detects repetitive Q&A patterns (many-shot jailbreaking)
- Identifies sycophantic language
- Finds bias injection (gender, age, racial, socioeconomic, ability)
- Provides confidence scores for each detection

**Usage Example:**
```python
from app.services.adversarial.jailbreak_detector import JailbreakDetector

detector = JailbreakDetector()
result = await detector.detect_manipulation(question, answer)

print(f"Manipulation Score: {result['manipulation_score']}")
print(f"Is Manipulative: {result['is_manipulative']}")
print(f"Detected Attacks: {result['detected_attacks']}")
```

### 2. Constitutional AI

**Location:** `app/services/constitutional/`

**Components:**
- `principles.py` - Defines 5 constitutional principles
- `classifier.py` - Classifies content against principles
- `feedback_loop.py` - Meta-evaluates evaluations

**The 5 Principles:**
1. **Harmlessness** (30% weight) - No harmful content
2. **Fairness** (25% weight) - No discrimination or bias
3. **Privacy** (15% weight) - Respects privacy
4. **Truthfulness** (20% weight) - Factually accurate
5. **Helpfulness** (10% weight) - Actually helpful

**Usage Example:**
```python
from app.services.constitutional.classifier import ConstitutionalClassifier

classifier = ConstitutionalClassifier()
result = await classifier.classify_content(question, answer)

print(f"Overall Score: {result['overall_score']}")
print(f"Compliant: {result['is_compliant']}")
print(f"Violations: {result['violations']}")
```

### 3. Interpretability

**Location:** `app/services/interpretability/`

**Component:**
- `feature_analyzer.py` - Analyzes neural features

**What it does:**
- Simulates 50+ neural features across 5 categories
- Provides transparency into evaluation reasoning
- Detects bias indicators
- Calculates reasoning quality scores

**Feature Categories:**
- Reasoning circuits (e.g., Legal Citation Recognition)
- Factual knowledge (e.g., Citation Quality)
- Safety features (e.g., Factual Accuracy Verification)
- Bias indicators (e.g., Gender/Age/Racial Bias)
- Linguistic patterns (e.g., Professional Tone)

**Usage Example:**
```python
from app.services.interpretability.feature_analyzer import FeatureAnalyzer

analyzer = FeatureAnalyzer()
result = analyzer.analyze_text(answer, context_type="legal")

print(f"Top Features: {result['activated_features'][:5]}")
print(f"Reasoning Quality: {result['reasoning_quality']}")
print(f"Bias Indicators: {len(result['bias_indicators'])}")
```

### 4. Enhanced Judge

**Location:** `app/services/enhanced_judge.py`

**What it does:**
- Integrates all 3 safety modules into a unified evaluation pipeline
- Provides 3-phase evaluation:
  1. Security checks (adversarial + constitutional)
  2. Base evaluation (standard LLM judge)
  3. Optional meta-evaluation (self-improvement)

**Usage Example:**
```python
from app.services.enhanced_judge import enhanced_judge

result = await enhanced_judge.evaluate_criterion(
    question=question,
    answer=answer,
    criterion_name="LEGAL_ACCURACY",
    criterion_description="Accuracy of legal information",
    domain="legal",
    judge_model="gpt-4o-mini",
    enable_safety_checks=True,
    enable_interpretability=True,
    enable_meta_evaluation=False
)

print(f"Score: {result['score']}/100")
print(f"Risk Level: {result['security']['risk_level']}")
print(f"Blocked: {result.get('blocked', False)}")
```

## Research Foundations

All features are inspired by Anthropic research papers:

1. **Many-Shot Jailbreaking (2024)** - Adversarial detection
2. **Constitutional AI (2022)** - Safety principles framework
3. **Constitutional Classifiers (2025)** - Automated compliance checking
4. **Scaling Monosemanticity (2024)** - Feature-based interpretability
5. **Superposition Analysis** - Neural circuit understanding

## Important Notes on Implementation

### What's Real vs Simulated

**Real (Production-Ready):**
- Adversarial detection patterns (many-shot, sycophancy)
- Bias detection via keyword/pattern matching
- Constitutional principle framework
- Integration with Claude/GPT APIs for classification
- Robustness scoring algorithms

**Simulated (Proof-of-Concept):**
- **Feature analysis is pattern-based, not neural** - The interpretability module uses regex patterns to simulate feature detection. In production, this would use actual Sparse Autoencoders (SAEs) trained on model activations.
- **Detection rates are estimates** - The "95% detection" claims in the notebook are based on the test cases provided, not large-scale validation.
- **Constitutional classification uses API calls** - Real classification happens via Claude/GPT, not trained classifiers.

### Accuracy Claims

The notebook mentions several accuracy percentages:
- "95%+ detection of many-shot jailbreaking" - Based on 5 test cases
- "90%+ bias detection" - Based on 4 test cases
- "98%+ constitutional compliance" - Estimate, not validated

These are **demonstrations on small test sets**, not validated accuracy on large datasets.

### Performance

- Full enhanced evaluation adds ~2-4s overhead per evaluation
- Most time is spent on API calls to Claude/GPT
- Feature analysis is fast (<100ms)
- Can be toggled on/off via boolean flags

## Future Enhancements

To make this production-grade:

1. **Replace simulated features with real SAEs**
   - Use Anthropic's published SAE models
   - Extract actual neural activations

2. **Validate on large datasets**
   - Test on 1000+ adversarial examples
   - Calculate true accuracy metrics

3. **Add circuit steering**
   - Actively suppress bias circuits
   - Amplify safety circuits during evaluation

4. **Multi-judge ensemble**
   - Run multiple models (GPT-4o, Claude, Llama)
   - Use voting/consensus for robustness

5. **Automated red-teaming**
   - Generate adversarial attacks automatically
   - Continuous testing of system robustness

## API Reference

All modules use async/await patterns. Key methods:

```python
# Adversarial
await detector.detect_manipulation(question, answer)
bias_tester.test_for_bias(text)
scorer.calculate_robustness_score(jailbreak_results, bias_results)

# Constitutional
await classifier.classify_content(question, answer, check_all_principles=True)
await feedback_loop.meta_evaluate(evaluation, criterion, qa_context)

# Interpretability
analyzer.analyze_text(text, context_type="general")

# Enhanced Judge
await enhanced_judge.evaluate_criterion(
    question, answer, criterion_name, criterion_description,
    domain, judge_model, enable_safety_checks, enable_interpretability, enable_meta_evaluation
)
```

## Troubleshooting

**Import errors:**
```bash
# Make sure you're in the project root
cd /Users/aryanmarwah/Documents/LLMasjudge

# Activate venv
source llmjudgevenv/bin/activate

# Reinstall if needed
pip install -r requirements.txt
```

**API key errors:**
- Check `.env` file has `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`
- Constitutional classifier uses Claude by default
- Can fall back to GPT if Claude unavailable

**Jupyter kernel not found:**
```bash
# Reinstall kernel
source llmjudgevenv/bin/activate
python -m ipykernel install --user --name=llmjudgevenv --display-name="LLM Judge Research"
```

## Questions?

- Check `test_enhanced_features.py` for usage examples
- Run `demo.py` for interactive demonstrations
- See `examples/research_demo.ipynb` for research-oriented examples
