#!/bin/bash

# LLM Judge Platform - Startup Script
# This script starts the FastAPI backend and opens the frontend

set -e  # Exit on error

echo "🚀 Starting LLM Judge Platform..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with your API keys:"
    echo "  OPENAI_API_KEY=your-key-here"
    echo "  ANTHROPIC_API_KEY=your-key-here"
    echo ""
fi

# Check if backend dependencies are installed
echo "✅ Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "❌ Dependencies missing! Installing..."
    pip install -r requirements.txt
}

# Kill any process running on port 8000
echo "🧹 Cleaning up port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start backend server in background
echo "🔧 Starting FastAPI backend on http://localhost:8000..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

echo "   Backend PID: $BACKEND_PID"
echo "   Logs: tail -f backend.log"

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Backend failed to start. Check backend.log for errors."
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Check backend health
echo ""
echo "🏥 Backend Health Check:"
curl -s http://localhost:8000/api/health | python -m json.tool || echo "Failed to get health status"

# Open frontend in browser
echo ""
echo "🌐 Opening frontend in browser..."
sleep 1
open index.html

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ LLM Judge Platform is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: index.html (opened in browser)"
echo ""
echo "📊 View backend logs: tail -f backend.log"
echo "🛑 Stop backend: kill $BACKEND_PID"
echo ""
echo "Press Ctrl+C to stop monitoring (backend will keep running)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Monitor backend logs
tail -f backend.log
