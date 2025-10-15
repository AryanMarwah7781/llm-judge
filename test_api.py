#!/usr/bin/env python3
"""Quick test script to verify the API is working."""
import subprocess
import time
import requests
import sys
import os

# Change to project directory
os.chdir('/Users/aryanmarwah/Documents/LLMasjudge')

# Start the server in background
print("🚀 Starting FastAPI server...")
python_path = '/Users/aryanmarwah/Documents/LLMasjudge/.venv/bin/python'
server = subprocess.Popen(
    [python_path, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
print("⏳ Waiting for server to start...")
time.sleep(3)

try:
    # Test health endpoint
    print("\n📊 Testing /api/health endpoint...")
    response = requests.get('http://localhost:8000/api/health')
    
    if response.status_code == 200:
        print("✅ Health check successful!")
        print("\nResponse:")
        import json
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Health check failed with status code: {response.status_code}")
        sys.exit(1)
    
    # Test models endpoint
    print("\n📊 Testing /api/models endpoint...")
    response = requests.get('http://localhost:8000/api/models')
    
    if response.status_code == 200:
        print("✅ Models endpoint successful!")
        data = response.json()
        print(f"\nAvailable models: {len(data['models'])}")
        for model in data['models']:
            print(f"  - {model['name']} ({model['id']})")
    else:
        print(f"❌ Models endpoint failed with status code: {response.status_code}")
    
    # Test root endpoint
    print("\n📊 Testing root endpoint...")
    response = requests.get('http://localhost:8000/')
    
    if response.status_code == 200:
        print("✅ Root endpoint successful!")
        print("\nAPI Info:")
        import json
        print(json.dumps(response.json(), indent=2))
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\n📚 API Documentation available at:")
    print("   http://localhost:8000/docs (Swagger)")
    print("   http://localhost:8000/redoc (ReDoc)")
    print("\n⚠️  Note: To use the evaluation endpoint, add your API keys to .env file:")
    print("   OPENAI_API_KEY=sk-...")
    print("   ANTHROPIC_API_KEY=sk-ant-...")
    print("\n🛑 Server is still running. Press Ctrl+C to stop.")
    
    # Keep server running
    server.wait()
    
except KeyboardInterrupt:
    print("\n\n🛑 Stopping server...")
    server.terminate()
    server.wait()
    print("✅ Server stopped successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    server.terminate()
    server.wait()
    sys.exit(1)
