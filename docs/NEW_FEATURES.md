# New Features: Templates & Safety Checks

## Overview

Two new features have been added to the LLM Judge platform:

1. **Custom Criteria Templates** - Save and reuse evaluation criteria
2. **Lightweight Safety Checks** - Fast bias and adversarial detection

---

## 1. Custom Criteria Templates

### What It Does

Allows users to save criteria sets as templates for reuse across multiple evaluations.

### API Endpoints

#### Create Template
```bash
POST /api/templates
```

**Request Body:**
```json
{
  "name": "Legal Review Criteria",
  "domain": "legal",
  "description": "Standard criteria for legal document review",
  "criteria": [
    {
      "name": "CITATION_ACCURACY",
      "weight": 40,
      "hardMin": 90,
      "description": "Verify legal citations"
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": "tpl_20251019_123456",
  "name": "Legal Review Criteria",
  "domain": "legal",
  "description": "Standard criteria for legal document review",
  "criteria": [...],
  "created_at": "2025-10-19T12:34:56",
  "updated_at": "2025-10-19T12:34:56"
}
```

#### List Templates
```bash
GET /api/templates?domain=legal
```

**Response:** `200 OK`
```json
{
  "templates": [...]
}
```

#### Get Template
```bash
GET /api/templates/{template_id}
```

#### Update Template
```bash
PUT /api/templates/{template_id}
```

#### Delete Template
```bash
DELETE /api/templates/{template_id}
```

### Storage

Templates are stored in `data/templates.json` (not committed to git).

---

## 2. Lightweight Safety Checks

### What It Does

Before evaluation, performs fast pattern-based checks for:
- **Adversarial manipulation** - Many-shot jailbreaking, sycophancy
- **Bias** - Gender, age, racial, socioeconomic, ability bias

### Performance

- **Speed:** ~50-100ms overhead per Q&A pair
- **No API calls:** Pure pattern matching (free)
- **Opt-in:** Can be disabled with `enable_safety_checks=false`

### Integration

Safety checks are automatically included in the `/api/evaluate` endpoint:

```bash
POST /api/evaluate
```

**Form Data:**
- `file`: PDF/TXT file
- `criteria`: JSON string
- `judge_model`: Model to use
- `global_threshold`: Pass/fail threshold
- `domain`: Domain context
- `enable_safety_checks`: `true` (default) or `false`

**Response includes `safety_warnings`:**
```json
{
  "evaluations": [...],
  "summary": {...},
  "safety_warnings": [
    {
      "qa_index": 2,
      "question": "What is the best investment...",
      "warnings": [
        {
          "type": "manipulation",
          "severity": "high",
          "score": 0.850,
          "description": "Detected 2 manipulation pattern(s)",
          "attacks": ["many_shot_jailbreak", "sycophantic_language"]
        },
        {
          "type": "bias",
          "severity": "medium",
          "score": 0.650,
          "description": "Potential bias detected in: gender, age",
          "categories": ["gender", "age"]
        }
      ]
    }
  ]
}
```

### Detection Types

**Manipulation Detection:**
- Many-shot jailbreaking (repetitive Q&A patterns)
- Sycophantic language ("brilliant!", "you're so smart!")
- Categorical claims ("everyone knows", "always", "never")

**Bias Detection:**
- Gender bias (stereotypes about men/women)
- Age bias (ageist language about young/old)
- Racial bias (discriminatory language)
- Socioeconomic bias (class-based stereotypes)
- Ability bias (ableist language)

### Severity Levels

- **High:** Score > 0.7 - Likely problematic
- **Medium:** Score 0.6-0.7 - Worth reviewing
- **Low:** Score < 0.6 - Minor concerns

---

## Usage Example

### 1. Create and Save Template

```javascript
// Create template
const template = await fetch('/api/templates', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "Medical Review",
    domain: "medical",
    criteria: [
      { name: "ACCURACY", weight: 50, hardMin: 95, description: "Medical accuracy" },
      { name: "SAFETY", weight: 50, hardMin: 90, description: "Safety recommendations" }
    ]
  })
});

const saved = await template.json();
console.log(`Template ID: ${saved.id}`);
```

### 2. Load Template and Evaluate

```javascript
// Load template
const template = await fetch(`/api/templates/${templateId}`).then(r => r.json());

// Evaluate with template criteria + safety checks
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('criteria', JSON.stringify(template.criteria));
formData.append('judge_model', 'gpt-4o-mini');
formData.append('global_threshold', '85');
formData.append('domain', template.domain);
formData.append('enable_safety_checks', 'true');  // Enable safety

const results = await fetch('/api/evaluate', {
  method: 'POST',
  body: formData
}).then(r => r.json());

// Check for safety warnings
if (results.safety_warnings && results.safety_warnings.length > 0) {
  console.log(`⚠️ Found ${results.safety_warnings.length} Q&A pairs with warnings`);

  results.safety_warnings.forEach(warning => {
    console.log(`Q&A #${warning.qa_index}:`);
    warning.warnings.forEach(w => {
      console.log(`  - ${w.type}: ${w.description} (${w.severity})`);
    });
  });
}
```

---

## Frontend Integration TODO

### Templates UI

- [ ] "Save as Template" button on criteria step
- [ ] "Load Template" dropdown
- [ ] Template manager modal (view, edit, delete templates)
- [ ] Template preview before loading

### Safety Warnings UI

- [ ] Warning badges on Q&A pairs with issues
- [ ] Color-coding (green=clean, yellow=warnings, red=high-severity)
- [ ] Expandable warning details
- [ ] Toggle to enable/disable safety checks
- [ ] Safety summary in results header

---

## Testing

Run the test suite:

```bash
python3 test_new_features.py
```

Or test manually via API:

```bash
# Create template
curl -X POST http://localhost:8000/api/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Template",
    "domain": "general",
    "criteria": [...]
  }'

# List templates
curl http://localhost:8000/api/templates
```

---

## Performance Impact

### Templates

- **Storage:** JSON file (lightweight, fast)
- **API overhead:** Negligible (<10ms)
- **Scalability:** Good for 100s of templates

### Safety Checks

- **Per Q&A pair:** ~50-100ms
- **Total for 10 pairs:** ~0.5-1 second
- **Cost:** $0 (no API calls)
- **Accuracy:** Pattern-based (good for obvious cases)

**Example:**
- Without safety: 5 seconds
- With safety: 5.5-6 seconds (~10% overhead)

---

## Limitations

### Templates

- Currently stored locally (not synced across deployments)
- No user authentication (all users see all templates)
- No template versioning

**Future:** Use database (PostgreSQL) for multi-user support.

### Safety Checks

- Pattern-based (may miss novel attacks)
- No semantic understanding
- Can have false positives/negatives
- Not foolproof (supplement, not replacement)

**What it catches:** Obvious manipulation and bias patterns
**What it misses:** Subtle, novel, or rephrased attacks

---

## Configuration

### Disable Safety Checks

```python
# In frontend
formData.append('enable_safety_checks', 'false');
```

### Adjust Thresholds

Edit detection logic in:
- `app/services/adversarial/jailbreak_detector.py`
- `app/services/adversarial/bias_tester.py`

### Storage Location

Change template storage path:

```python
# In app/services/template_manager.py
template_manager = TemplateManager(storage_path="custom/path/templates.json")
```

---

## Next Steps

1. **Frontend Integration** - Add UI for templates and safety warnings
2. **Database Migration** - Move from JSON to PostgreSQL
3. **User Authentication** - Per-user templates
4. **Advanced Safety** - Semantic understanding, ML-based detection
5. **Template Sharing** - Export/import templates

---

## API Documentation

Full API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Template endpoints are under the "templates" tag.
Safety warnings are included in evaluation responses.
