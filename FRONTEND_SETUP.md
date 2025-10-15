# Frontend Setup Guide

## Quick Start

You now have a fully functional React frontend that connects to your FastAPI backend!

### Option 1: Open HTML File Directly (Easiest)

1. **Make sure your backend is running:**
   ```bash
   cd /Users/aryanmarwah/Documents/LLMasjudge
   source .venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the frontend:**
   - Simply open `index.html` in your browser:
   ```bash
   open index.html
   ```
   
   Or drag and drop `index.html` into Chrome/Firefox/Safari

3. **That's it!** The frontend will connect to `http://localhost:8000`

### Option 2: Run with a Local Server (Recommended for CORS)

If you encounter CORS issues, run a simple HTTP server:

```bash
# Using Python
python3 -m http.server 3000

# Or using Node.js (if you have it)
npx serve .
```

Then open: `http://localhost:3000`

---

## How to Use the Frontend

### 1. **Select Domain** (Step 1)
- Choose from Legal, Medical, or Finance
- Each domain has pre-configured criteria optimized for that field
- Legal domain is recommended for testing with your `law_questions.pdf`

### 2. **Review Criteria** (Step 2)
- See the evaluation criteria and their weights
- Each criterion has a hard minimum threshold
- Weights must sum to 100%

### 3. **Upload PDF & Select Model** (Step 3)
- **Upload your PDF** containing Q&A pairs
- **Select a judge model:**
  - `CLAUDE_SONNET_4.5` → claude-sonnet-4 (Best quality, $0.03/eval)
  - `GPT-4O` → gpt-4o (Fast, $0.025/eval)
  - `GPT-4O-MINI` → gpt-4o-mini (Cheapest, $0.002/eval)

### 4. **View Results** (Step 4)
- See pass/fail verdicts for each Q&A pair
- View detailed scores for each criterion
- See which criteria passed/failed
- Check average scores and pass rates

---

## Testing with Your Law Questions

1. Start backend:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Open `index.html` in browser

3. Follow the wizard:
   - Select **LEGAL** domain
   - Review criteria (CITATION_ACCURACY, LEGAL_REASONING, etc.)
   - Upload `law_questions.pdf`
   - Select **CLAUDE_SONNET_4.5** (recommended)
   - Click **RUN_EVALUATION**

4. Wait for results (usually 10-30 seconds)

5. Review detailed scores and pass/fail verdicts

---

## Troubleshooting

### Backend Not Running
**Error:** `Failed to evaluate. Make sure the backend is running...`

**Solution:**
```bash
cd /Users/aryanmarwah/Documents/LLMasjudge
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### CORS Issues
**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:** Your backend already has CORS enabled. If you still see issues:
1. Make sure you're running the backend on port 8000
2. Try using a local server (Option 2 above)
3. Check browser console for specific CORS errors

### API Key Issues
**Error:** `Missing API key` or authentication errors

**Solution:**
```bash
# Make sure .env has your keys
cat .env

# Should contain:
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

### PDF Upload Issues
**Error:** `No Q&A pairs found in PDF`

**Solution:** Make sure your PDF contains Q&A pairs in one of these formats:
```
Q: Question text?
A: Answer text.

Question: Question text?
Answer: Answer text.

**Q:** Question text?
**A:** Answer text.

1. Question text?
   Answer text.
```

---

## Customizing the Frontend

### Change API URL
If your backend is on a different port or URL, edit `index.html`:

```javascript
// Line ~115
const API_BASE_URL = 'http://localhost:8000';  // Change this
```

### Modify Criteria Presets
Edit the `suggestCriteria` function in `index.html` (around line 120):

```javascript
const criteriaMap = {
  legal: [
    { name: 'CITATION_ACCURACY', weight: 40, hardMin: 90, description: 'Verify legal citations' },
    // Add or modify criteria here
  ],
  // ...
};
```

### Add New Judge Models
Edit the model list in `ModelSelection` component (around line 480):

```javascript
{[
  {
    name: 'NEW_MODEL',
    speed: 'FAST',
    cost: '$0.XX',
    accuracy: 'XX%',
  },
  // ...
]}
```

Then update the model mapping (around line 165):

```javascript
const modelMap = {
  'NEW_MODEL': 'backend-model-name',
  // ...
};
```

---

## Next Steps

### Deploy Frontend
1. **Vercel/Netlify:** Simply upload `index.html`
2. **GitHub Pages:** Push to repo and enable Pages
3. **With Backend:** Serve from FastAPI using static files

### Add Features
- [ ] Batch evaluation (multiple PDFs)
- [ ] Custom criteria editor
- [ ] Results export (JSON/CSV)
- [ ] Evaluation history
- [ ] Real-time progress updates
- [ ] Side-by-side model comparison

### Production Considerations
- Add proper error boundaries
- Implement request cancellation
- Add retry logic for failed requests
- Show estimated cost before running
- Add authentication for multi-user deployments

---

## API Endpoints Reference

Your backend exposes these endpoints:

### Health Check
```bash
GET http://localhost:8000/api/health
```

### Available Models
```bash
GET http://localhost:8000/api/models
```

### Evaluate Q&A Pairs
```bash
POST http://localhost:8000/api/evaluate
Content-Type: multipart/form-data

Fields:
- file: PDF file
- criteria: JSON array of criteria objects
- judge_model: "claude-sonnet-4" | "gpt-4o" | "gpt-4o-mini"
```

---

## Example Request

```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('criteria', JSON.stringify([
  {
    name: 'CITATION_ACCURACY',
    weight: 100,
    hardMin: 80,
    description: 'Verify legal citations are accurate'
  }
]));
formData.append('judge_model', 'claude-sonnet-4');

const response = await fetch('http://localhost:8000/api/evaluate', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data);
```

---

## Support

- **Backend Issues:** Check `app/main.py` logs
- **Frontend Issues:** Check browser console (F12)
- **API Issues:** Test with `curl` or Postman first
- **CORS Issues:** Verify backend CORS configuration in `app/main.py`

---

**Your system is now fully connected! 🎉**

Start the backend, open `index.html`, and start evaluating!
