# 🚀 How to Start the LLM Judge Platform

## Quick Start (Easiest Method)

### Option 1: One-Command Startup Script

```bash
./start.sh
```

That's it! This will:
- ✅ Activate virtual environment
- ✅ Check dependencies
- ✅ Start backend on port 8000
- ✅ Open frontend in your browser
- ✅ Show live logs

### Option 2: Manual Startup (Step by Step)

#### Step 1: Start Backend
```bash
cd /Users/aryanmarwah/Documents/LLMasjudge
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 2: Open Frontend
In a new terminal or browser:
```bash
open index.html
```

Or simply drag `index.html` into your browser.

---

## Stopping the App

### Option 1: Use Stop Script
```bash
./stop.sh
```

### Option 2: Manual Stop
If backend is running in terminal:
```bash
# Press Ctrl+C in the terminal running uvicorn
```

If backend is running in background:
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Verification

### Check if Backend is Running
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "api_keys_configured": {
    "openai": true,
    "anthropic": true
  }
}
```

### Check Available Endpoints
```bash
# View API documentation
open http://localhost:8000/docs

# Or check available models
curl http://localhost:8000/api/models
```

---

## Typical Workflow

### 1. **Start the app:**
```bash
./start.sh
```

### 2. **Use the frontend:**
- Browser opens automatically
- Select domain (Legal/Medical/Finance)
- Review criteria
- Upload PDF with Q&A pairs
- Select judge model
- Run evaluation
- View results

### 3. **Stop when done:**
```bash
./stop.sh
```

---

## Alternative: Keep Backend Running Permanently

If you want the backend to run continuously:

```bash
# Start in background (daemon mode)
source .venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# Save the process ID
echo $! > backend.pid

# Stop it later
kill $(cat backend.pid)
```

---

## Troubleshooting

### Port 8000 Already in Use
```bash
# Find what's using port 8000
lsof -ti:8000

# Kill it
lsof -ti:8000 | xargs kill -9

# Or use the stop script
./stop.sh
```

### Virtual Environment Not Activated
```bash
source .venv/bin/activate
```

### Dependencies Missing
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### API Keys Not Configured
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
EOF
```

### Backend Not Responding
```bash
# Check logs
tail -f backend.log

# Or run in foreground to see errors
uvicorn app.main:app --reload
```

---

## Development Mode

For active development with hot reloading:

```bash
# Terminal 1: Backend with auto-reload
source .venv/bin/activate
uvicorn app.main:app --reload --log-level debug

# Terminal 2: Watch logs
tail -f backend.log

# Browser: Open index.html
# Frontend automatically connects to backend
```

---

## Production Mode

For production deployment:

```bash
# Use production ASGI server
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use the Docker setup:
```bash
docker-compose up -d
```

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| **Start everything** | `./start.sh` |
| **Stop everything** | `./stop.sh` |
| **Start backend only** | `uvicorn app.main:app --reload` |
| **Open frontend** | `open index.html` |
| **Check health** | `curl localhost:8000/api/health` |
| **View API docs** | `open http://localhost:8000/docs` |
| **View logs** | `tail -f backend.log` |
| **Kill backend** | `lsof -ti:8000 \| xargs kill -9` |
| **Restart** | `./stop.sh && ./start.sh` |

---

## What Happens When You Start?

1. **Virtual environment activates** → Ensures Python packages are isolated
2. **Dependencies check** → Verifies all required packages installed
3. **Port cleanup** → Kills any stale processes on port 8000
4. **Backend starts** → FastAPI server launches on http://localhost:8000
5. **Health check** → Waits for backend to be ready (max 10 seconds)
6. **Frontend opens** → Opens index.html in your default browser
7. **Monitoring** → Shows live backend logs

---

## URLs You Can Access

Once started, these URLs are available:

- **Frontend UI**: `file:///Users/aryanmarwah/Documents/LLMasjudge/index.html`
- **Backend API**: http://localhost:8000
- **API Health**: http://localhost:8000/api/health
- **API Models**: http://localhost:8000/api/models
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## First Time Setup

If this is your first time:

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env with your API keys
cp .env.example .env  # If exists
# Or create manually:
echo "OPENAI_API_KEY=your-key" > .env
echo "ANTHROPIC_API_KEY=your-key" >> .env

# 5. Verify setup
python verify_setup.py

# 6. Start the app
./start.sh
```

---

## Next Steps

After starting:
1. ✅ Backend will be at http://localhost:8000
2. ✅ Frontend will open in your browser
3. ✅ Try evaluating `law_questions.pdf`
4. ✅ Check browser console (F12) for detailed logs
5. ✅ View API request log in bottom-right corner

**You're all set! 🎉**
