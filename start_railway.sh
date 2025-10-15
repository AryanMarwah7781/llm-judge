#!/bin/bash
# Railway startup script - handles PORT environment variable

# Railway provides PORT as an environment variable
# Default to 8000 if PORT is not set (for local testing)
PORT=${PORT:-8000}

echo "🚀 Starting uvicorn on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
