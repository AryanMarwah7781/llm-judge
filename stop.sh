#!/bin/bash

# LLM Judge Platform - Stop Script

echo "🛑 Stopping LLM Judge Platform..."

# Kill backend process on port 8000
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "   Killing backend process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo "✅ Backend stopped"
else
    echo "ℹ️  Backend is not running"
fi

# Remove log file
if [ -f "backend.log" ]; then
    rm backend.log
    echo "🧹 Cleaned up backend.log"
fi

echo "✨ All stopped!"
