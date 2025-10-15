# Quick Start Guide

Get your LLM Judge API running in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API key OR Anthropic API key (at least one)

## Step 1: Install Dependencies (1 minute)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all required packages
pip install -r requirements.txt
```

## Step 2: Configure API Keys (1 minute)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# You need at least ONE of these:
nano .env  # or use your preferred editor
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

## Step 3: Verify Setup (30 seconds)

```bash
python verify_setup.py
```

You should see all green checkmarks ✅

## Step 4: Start the Server (30 seconds)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 5: Test the API (2 minutes)

### Option A: Use the Interactive Docs

Open your browser and go to:
```
http://localhost:8000/docs
```

Try the `/api/health` endpoint first!

### Option B: Use curl

```bash
# Health check
curl http://localhost:8000/api/health

# Get available models
curl http://localhost:8000/api/models
```

### Option C: Use the Example Script

```bash
python example_usage.py
```

## Your First Evaluation

### Create a test file: `test_qa.md`

```markdown
Q: What is 2+2?

A: The answer is 4. This is a basic arithmetic operation.

---

Q: What is the capital of France?

A: The capital of France is Paris, located in the north-central part of the country.
```

### Convert to PDF

Use any online Markdown to PDF converter, or if you have `pandoc`:

```bash
pandoc test_qa.md -o test_qa.pdf
```

### Evaluate!

```bash
curl -X POST "http://localhost:8000/api/evaluate" \
  -F "file=@test_qa.pdf" \
  -F 'criteria=[
    {
      "name": "ACCURACY",
      "weight": 50,
      "hardMin": 70,
      "description": "Factual accuracy of the answer"
    },
    {
      "name": "CLARITY",
      "weight": 50,
      "hardMin": 60,
      "description": "Clarity and readability"
    }
  ]' \
  -F "judge_model=gpt-4o-mini" \
  -F "global_threshold=75"
```

## Common Issues & Solutions

### Issue: "Module not found"
**Solution:** Make sure you activated the virtual environment and installed requirements
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Install packages
```

### Issue: "API key not configured"
**Solution:** Check your `.env` file has actual API keys (not placeholder text)

### Issue: "No Q&A pairs found"
**Solution:** Ensure your PDF has clearly formatted Q&A pairs
- Use "Q:" and "A:" or "Question:" and "Answer:"
- Separate Q&A pairs with blank lines
- See `sample_qa_pairs.md` for examples

### Issue: "Port 8000 already in use"
**Solution:** Use a different port
```bash
uvicorn app.main:app --reload --port 8001
```

## Next Steps

1. **Read the README.md** for detailed documentation
2. **Read DESIGN.md** to understand the architecture
3. **Customize criteria** for your use case
4. **Deploy to production** using Railway, Render, or Docker

## Production Deployment

### Quick Deploy to Railway

1. Push to GitHub
2. Go to railway.app
3. Create new project from GitHub repo
4. Add environment variables (API keys)
5. Deploy! 🚀

### Quick Deploy to Render

1. Push to GitHub
2. Go to render.com
3. New Web Service → Connect repo
4. Add environment variables
5. Deploy! 🚀

## Getting Help

- Check the logs: Look at terminal output for errors
- API documentation: http://localhost:8000/docs
- Example code: `example_usage.py`
- Design docs: `DESIGN.md`

## Success Checklist

- [ ] Virtual environment created and activated
- [ ] Requirements installed successfully
- [ ] `.env` file created with API keys
- [ ] `verify_setup.py` shows all checks passed
- [ ] Server starts without errors
- [ ] `/api/health` endpoint returns healthy status
- [ ] `/api/models` endpoint returns model list
- [ ] Successfully evaluated a test PDF

Once all items are checked, you're ready to go! 🎉

## Pro Tips

1. **Use GPT-4o-mini for testing** - It's faster and cheaper
2. **Start with simple criteria** - Add complexity gradually
3. **Check the logs** - They show detailed information about what's happening
4. **Use async** - The API handles multiple requests efficiently
5. **Monitor costs** - Keep track of LLM API usage

## Need More Help?

- Email support (add your contact)
- GitHub Issues: (add your repo URL)
- Documentation: Check README.md and DESIGN.md

Happy evaluating! 🚀
