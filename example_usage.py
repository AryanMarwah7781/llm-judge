"""Example script demonstrating API usage."""
import requests
import json


def evaluate_qa_pairs():
    """Example: Evaluate Q&A pairs from a PDF."""
    
    # API endpoint
    url = "http://localhost:8000/api/evaluate"
    
    # Define evaluation criteria
    criteria = [
        {
            "name": "CITATION_ACCURACY",
            "weight": 30,
            "hardMin": 70,
            "description": "Accuracy and completeness of citations and references"
        },
        {
            "name": "RELEVANCE",
            "weight": 25,
            "hardMin": 60,
            "description": "How relevant and on-topic the answer is to the question"
        },
        {
            "name": "CLARITY",
            "weight": 25,
            "hardMin": 60,
            "description": "Clarity, readability, and structure of the answer"
        },
        {
            "name": "COMPLETENESS",
            "weight": 20,
            "hardMin": 65,
            "description": "How complete and thorough the answer is"
        }
    ]
    
    # Prepare request
    files = {
        "file": open("sample_qa_pairs.pdf", "rb")  # Your PDF file
    }
    
    data = {
        "criteria": json.dumps(criteria),
        "judge_model": "gpt-4o",  # or "gpt-4o-mini", "claude-sonnet-4"
        "global_threshold": 85,
        "domain": "legal"  # or "medical", "finance", "general"
    }
    
    # Make request
    print("Sending evaluation request...")
    response = requests.post(url, files=files, data=data)
    
    # Check response
    if response.status_code == 200:
        results = response.json()
        print("\n✅ Evaluation Complete!")
        print(f"\nSummary:")
        print(f"  Total Q&As: {results['summary']['total']}")
        print(f"  Passed: {results['summary']['passed']}")
        print(f"  Failed: {results['summary']['failed']}")
        print(f"  Average Score: {results['summary']['avg_score']:.2f}")
        
        # Print detailed results
        print("\nDetailed Results:")
        for evaluation in results['evaluations']:
            print(f"\n{'='*60}")
            print(f"Q&A #{evaluation['qa_id']}: {evaluation['verdict']}")
            print(f"Weighted Score: {evaluation['weighted_score']:.2f}")
            print(f"\nQuestion: {evaluation['question'][:100]}...")
            print(f"\nCriterion Scores:")
            for criterion, score_data in evaluation['scores'].items():
                status = "✓" if score_data['passed'] else "✗"
                print(f"  {status} {criterion}: {score_data['score']:.0f}/100")
                print(f"     {score_data['reasoning'][:80]}...")
                if score_data['issues']:
                    print(f"     Issues: {', '.join(score_data['issues'])}")
            
            if evaluation['reason']:
                print(f"\nRejection Reason: {evaluation['reason']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())


def check_health():
    """Example: Check API health."""
    response = requests.get("http://localhost:8000/api/health")
    
    if response.status_code == 200:
        health = response.json()
        print("✅ API is healthy")
        print(f"Version: {health['version']}")
        print(f"OpenAI configured: {health['api_keys_configured']['openai']}")
        print(f"Anthropic configured: {health['api_keys_configured']['anthropic']}")
    else:
        print("❌ API is not healthy")


def get_available_models():
    """Example: Get available judge models."""
    response = requests.get("http://localhost:8000/api/models")
    
    if response.status_code == 200:
        data = response.json()
        print("Available Judge Models:\n")
        for model in data['models']:
            print(f"📊 {model['name']} ({model['id']})")
            print(f"   Provider: {model['provider']}")
            print(f"   Description: {model['description']}")
            print(f"   Context Window: {model['context_window']:,} tokens")
            print(f"   Input Cost: ${model['cost_per_1k_tokens']['input']}/1k tokens")
            print(f"   Output Cost: ${model['cost_per_1k_tokens']['output']}/1k tokens")
            print()


if __name__ == "__main__":
    print("LLM as Judge - API Examples\n")
    
    # Check health
    print("1. Checking API health...")
    check_health()
    print()
    
    # Get models
    print("2. Getting available models...")
    get_available_models()
    print()
    
    # Evaluate (uncomment when you have a PDF file)
    # print("3. Evaluating Q&A pairs...")
    # evaluate_qa_pairs()
