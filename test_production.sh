#!/bin/bash

echo "=================================================="
echo "Testing LLM Judge - Templates & Safety Features"
echo "=================================================="
echo ""

# Test 1: Health Check
echo "1. Testing backend health..."
curl -s http://127.0.0.1:8000/ | python3 -m json.tool
echo ""

# Test 2: List templates (legal)
echo "2. Listing legal templates..."
curl -s "http://127.0.0.1:8000/api/templates?domain=legal" | python3 -m json.tool
echo ""

# Test 3: Create a test template
echo "3. Creating test template..."
curl -s -X POST http://127.0.0.1:8000/api/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Template - Auto Created",
    "domain": "legal",
    "description": "Auto-created test template",
    "criteria": [
      {"name": "CITATION_ACCURACY", "weight": 40, "hardMin": 90, "description": "Verify legal citations"},
      {"name": "LEGAL_REASONING", "weight": 30, "hardMin": 80, "description": "Check legal logic"},
      {"name": "JURISDICTION", "weight": 20, "hardMin": 85, "description": "Verify court jurisdiction"},
      {"name": "FABRICATION_DETECT", "weight": 10, "hardMin": 95, "description": "Detect hallucinations"}
    ]
  }' | python3 -m json.tool
echo ""

# Test 4: List templates again (should see new one)
echo "4. Verifying template created..."
curl -s "http://127.0.0.1:8000/api/templates?domain=legal" | python3 -m json.tool
echo ""

echo "=================================================="
echo "✓ All tests completed!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Visit http://127.0.0.1:8000 in your browser"
echo "2. Select 'Legal' domain"
echo "3. You should see 'Test Template - Auto Created' in dropdown"
echo "4. Production sites should deploy in 2-5 minutes"
echo ""
