"""Judge prompt templates for LLM evaluation."""
from typing import Dict, Any


def get_evaluation_prompt(
    domain: str,
    question: str,
    answer: str,
    criterion_name: str,
    criterion_description: str
) -> str:
    """
    Generate evaluation prompt for LLM judge.
    
    Args:
        domain: Domain context (legal, medical, finance, general)
        question: The question being evaluated
        answer: The answer to evaluate
        criterion_name: Name of the criterion to score
        criterion_description: Description of the criterion
    
    Returns:
        Formatted prompt string
    """
    domain_context = _get_domain_context(domain)
    
    prompt = f"""You are an expert evaluator assessing the quality of Q&A pairs in the {domain} domain.

{domain_context}

EVALUATION TASK:
You must evaluate the following answer based on the criterion: {criterion_name}

CRITERION DESCRIPTION:
{criterion_description}

QUESTION:
{question}

ANSWER:
{answer}

EVALUATION INSTRUCTIONS:
1. Carefully analyze the answer against the {criterion_name} criterion
2. Assign a score from 0 to 100:
   - 0-20: Poor/Completely inadequate
   - 21-40: Below average/Major issues
   - 41-60: Average/Moderate issues
   - 61-80: Good/Minor issues
   - 81-100: Excellent/No issues

3. Provide detailed reasoning explaining your score
4. List specific issues found (if any)

RESPONSE FORMAT:
You must respond with a valid JSON object (no markdown formatting):
{{
    "score": <number between 0-100>,
    "reasoning": "<detailed explanation of the score>",
    "issues": ["<specific issue 1>", "<specific issue 2>", ...]
}}

If there are no issues, use an empty array for issues.

Respond ONLY with the JSON object, no additional text or markdown formatting.
"""
    return prompt


def _get_domain_context(domain: str) -> str:
    """Get domain-specific context for evaluation."""
    contexts = {
        "legal": """
DOMAIN CONTEXT:
You are evaluating legal Q&A pairs. Pay special attention to:
- Accuracy of legal citations and references
- Proper use of legal terminology
- Completeness of legal analysis
- Adherence to jurisdictional considerations
- Ethical considerations and disclaimers
""",
        "medical": """
DOMAIN CONTEXT:
You are evaluating medical Q&A pairs. Pay special attention to:
- Medical accuracy and evidence-based information
- Proper use of medical terminology
- Patient safety considerations
- Appropriate disclaimers about seeking professional medical advice
- Citation of medical literature where applicable
""",
        "finance": """
DOMAIN CONTEXT:
You are evaluating financial Q&A pairs. Pay special attention to:
- Accuracy of financial information and calculations
- Proper use of financial terminology
- Risk disclosures and disclaimers
- Compliance with financial regulations
- Citation of sources for financial data
""",
        "general": """
DOMAIN CONTEXT:
You are evaluating general knowledge Q&A pairs. Pay special attention to:
- Factual accuracy and correctness
- Clarity and comprehensiveness
- Logical coherence
- Appropriate level of detail
- Proper citation of sources when needed
"""
    }
    return contexts.get(domain.lower(), contexts["general"])


def get_system_prompt() -> str:
    """Get system prompt for LLM judge."""
    return """You are an expert evaluator designed to assess the quality of question-answer pairs across multiple criteria. 

Your role is to:
1. Analyze answers objectively and thoroughly
2. Assign accurate scores based on specific criteria
3. Provide clear, actionable reasoning
4. Identify specific issues when they exist
5. Be consistent and fair in your evaluations

Always respond with valid JSON format as specified in the user prompt.
Do not include markdown code blocks or any additional formatting.
"""
