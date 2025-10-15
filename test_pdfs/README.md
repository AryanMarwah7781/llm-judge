# Test Q&A Files for LLM Judge Platform

This folder contains 12 test files with different scenarios to thoroughly test the evaluation platform.

## 📁 Test Files Overview:

### ✅ **Perfect Answers (Should Score High)**

**01_general_knowledge_perfect.txt**
- 10 Q&A pairs with detailed, accurate answers
- Topics: Geography, Math, Literature, Science, History
- Expected: High scores (90-100) across all criteria

**04_science_advanced.txt**
- 3 complex scientific questions
- Topics: Relativity, Quantum Mechanics, Water Cycle
- Expected: High scores for completeness and accuracy

**07_legal_accurate.txt**
- 5 legal questions with proper citations
- Topics: Case law, Legal principles
- Expected: Perfect citation accuracy, high legal reasoning

**08_science_comprehensive.txt**
- 5 detailed science questions
- Topics: Physics, Biology, Earth Science
- Expected: High completeness and clarity scores

---

### ❌ **Incorrect Answers (Should Score Low)**

**02_general_knowledge_incorrect.txt**
- Same 10 questions as file #1, but with wrong answers
- Expected: Low accuracy scores (0-30)
- Tests: Factual correctness detection

---

### ⚠️ **Incomplete Answers (Should Score Medium)**

**03_general_knowledge_incomplete.txt**
- Same questions with brief, incomplete answers
- Expected: Medium scores (40-70)
- Tests: Completeness criterion

**09_vague_answers.txt**
- Questions with vague, uncertain answers
- Expected: Low-medium scores (30-60)
- Tests: Clarity and confidence detection

---

### 🎯 **Specialized Topics**

**05_technology_detailed.txt**
- 5 tech questions with comprehensive answers
- Topics: Python, Databases, ML, Cloud, Cybersecurity
- Expected: High scores for domain expertise

**06_math_problems.txt**
- 5 math questions with formulas and explanations
- Topics: Geometry, Calculus, Number Theory
- Expected: High accuracy, good formatting

**10_sports_trivia.txt**
- 5 sports questions with factual answers
- Topics: World Cup, Olympics, Basketball
- Expected: High accuracy for specific facts

**11_arts_and_literature.txt**
- 5 questions on arts, music, and literature
- Topics: Renaissance, Impressionism, Classic Literature
- Expected: High scores for cultural knowledge

**12_emerging_technology.txt**
- 5 questions on cutting-edge tech
- Topics: Blockchain, AI, IoT, 5G, Crypto
- Expected: High scores for current tech understanding

---

## 🧪 Testing Strategies:

### **Test 1: Accuracy**
```bash
# Upload: 02_general_knowledge_incorrect.txt
# Criteria: ACCURACY (weight: 100, hardMin: 70)
# Expected: All questions fail, 0% pass rate
```

### **Test 2: Completeness**
```bash
# Upload: 03_general_knowledge_incomplete.txt
# Criteria: COMPLETENESS (weight: 100, hardMin: 70)
# Expected: Most questions fail, incomplete answers detected
```

### **Test 3: Multiple Criteria**
```bash
# Upload: 01_general_knowledge_perfect.txt
# Criteria:
#   - ACCURACY (weight: 40, hardMin: 70)
#   - COMPLETENESS (weight: 30, hardMin: 60)
#   - CLARITY (weight: 30, hardMin: 50)
# Expected: High scores across all criteria, 100% pass rate
```

### **Test 4: Legal Citations**
```bash
# Upload: 07_legal_accurate.txt
# Criteria:
#   - CITATION_ACCURACY (weight: 50, hardMin: 80)
#   - LEGAL_REASONING (weight: 50, hardMin: 70)
# Expected: Perfect citation scores
```

### **Test 5: Domain Expertise**
```bash
# Upload: 05_technology_detailed.txt
# Criteria:
#   - TECHNICAL_ACCURACY (weight: 60, hardMin: 70)
#   - DEPTH (weight: 40, hardMin: 60)
# Expected: High technical understanding scores
```

---

## 📊 Expected Results Summary:

| File | Expected Pass Rate | Key Testing Focus |
|------|-------------------|-------------------|
| 01 - Perfect | 90-100% | Baseline for good answers |
| 02 - Incorrect | 0-10% | Factual error detection |
| 03 - Incomplete | 30-50% | Completeness checking |
| 04 - Advanced | 80-95% | Complex topic handling |
| 05 - Technology | 85-100% | Domain expertise |
| 06 - Math | 90-100% | Formula and precision |
| 07 - Legal | 95-100% | Citation accuracy |
| 08 - Science | 90-100% | Comprehensive answers |
| 09 - Vague | 20-40% | Clarity detection |
| 10 - Sports | 85-95% | Factual trivia |
| 11 - Arts | 85-95% | Cultural knowledge |
| 12 - Emerging Tech | 80-95% | Current knowledge |

---

## 🚀 Quick Test Commands:

### Test via curl:
```bash
# Test perfect answers
curl -X POST https://your-backend-url/api/evaluate \
  -F "file=@01_general_knowledge_perfect.txt" \
  -F 'criteria=[{"name":"ACCURACY","weight":100,"hardMin":70}]' \
  -F "judge_model=gpt-4o-mini"

# Test incorrect answers
curl -X POST https://your-backend-url/api/evaluate \
  -F "file=@02_general_knowledge_incorrect.txt" \
  -F 'criteria=[{"name":"ACCURACY","weight":100,"hardMin":70}]' \
  -F "judge_model=gpt-4o-mini"

# Test with multiple criteria
curl -X POST https://your-backend-url/api/evaluate \
  -F "file=@08_science_comprehensive.txt" \
  -F 'criteria=[
    {"name":"ACCURACY","weight":40,"hardMin":70},
    {"name":"COMPLETENESS","weight":30,"hardMin":60},
    {"name":"CLARITY","weight":30,"hardMin":50}
  ]' \
  -F "judge_model=gpt-4o-mini"
```

---

## 💡 Testing Tips:

1. **Start with file #01 (perfect)** - Establish a baseline
2. **Test file #02 (incorrect)** - Verify error detection works
3. **Try different judge models** - Compare gpt-4o-mini vs claude-sonnet-4
4. **Vary hard minimums** - Test threshold sensitivity
5. **Use multiple criteria** - Test weighted scoring
6. **Check edge cases** - Files #03 and #09 test boundary conditions

---

## 📝 Notes:

- All files are in simple text format for easy PDF conversion
- Questions use clear Q:/A: formatting
- Some files also support numbered format (1. Question:)
- Answers vary from one-word to multi-paragraph
- Mix of technical and general knowledge topics

---

## 🎯 Creating Your Own Test Files:

Format your Q&A pairs like this:

```
Q: Your question here?
A: Your answer here with as much detail as needed.

Q: Another question?
A: Another answer.
```

Or numbered format:

```
1. Question: Your question here?
   Answer: Your answer here.

2. Question: Another question?
   Answer: Another answer.
```

---

**Happy Testing!** 🚀
