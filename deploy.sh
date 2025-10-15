#!/bin/bash

# LLM Judge Platform - Deployment Script
# Helps deploy to various platforms

set -e

PLATFORM=${1:-"help"}

echo "🚀 LLM Judge Platform - Deployment Helper"
echo ""

case $PLATFORM in
  "railway")
    echo "📦 Preparing for Railway deployment..."
    echo ""
    echo "Steps to deploy to Railway:"
    echo "1. Push your code to GitHub"
    echo "2. Go to https://railway.app"
    echo "3. Click 'Start a New Project' → 'Deploy from GitHub repo'"
    echo "4. Select this repository"
    echo "5. Add environment variables:"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    echo "Railway will automatically detect Python and deploy!"
    ;;

  "render")
    echo "📦 Preparing for Render deployment..."
    echo ""
    
    # Create render.yaml if it doesn't exist
    if [ ! -f "render.yaml" ]; then
      cat > render.yaml << 'EOF'
services:
  - type: web
    name: llm-judge
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
EOF
      echo "✅ Created render.yaml"
    fi
    
    echo "Steps to deploy to Render:"
    echo "1. Push your code to GitHub"
    echo "2. Go to https://render.com"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect your GitHub repository"
    echo "5. Render will use render.yaml automatically"
    echo "6. Add your API keys in environment variables"
    ;;

  "fly")
    echo "📦 Preparing for Fly.io deployment..."
    echo ""
    
    # Check if flyctl is installed
    if ! command -v flyctl &> /dev/null; then
      echo "⚠️  Fly CLI not found. Installing..."
      brew install flyctl || curl -L https://fly.io/install.sh | sh
    fi
    
    # Check if fly.toml exists
    if [ ! -f "fly.toml" ]; then
      echo "Creating fly.toml..."
      flyctl launch --no-deploy
    fi
    
    echo "Setting secrets..."
    echo "Please enter your OpenAI API key:"
    read -s OPENAI_KEY
    flyctl secrets set OPENAI_API_KEY="$OPENAI_KEY"
    
    echo "Please enter your Anthropic API key:"
    read -s ANTHROPIC_KEY
    flyctl secrets set ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
    
    echo "Deploying to Fly.io..."
    flyctl deploy
    
    echo "✅ Deployed! Your app is live at:"
    flyctl status
    ;;

  "vercel")
    echo "📦 Deploying frontend to Vercel..."
    echo ""
    
    # Check if vercel is installed
    if ! command -v vercel &> /dev/null; then
      echo "⚠️  Vercel CLI not found. Installing..."
      npm i -g vercel
    fi
    
    # Create vercel.json
    cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
EOF
    
    echo "Deploying to Vercel..."
    vercel --prod
    
    echo ""
    echo "✅ Frontend deployed!"
    echo "⚠️  Don't forget to update API_BASE_URL in index.html to your backend URL"
    ;;

  "docker")
    echo "🐳 Building and running with Docker..."
    echo ""
    
    docker-compose down 2>/dev/null || true
    docker-compose build
    docker-compose up -d
    
    echo "✅ Running at http://localhost:8000"
    echo "View logs: docker-compose logs -f"
    ;;

  "github")
    echo "📦 Preparing for GitHub deployment..."
    echo ""
    
    if [ ! -d ".git" ]; then
      echo "Initializing git repository..."
      git init
      
      # Create .gitignore
      cat > .gitignore << 'EOF'
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.venv/
venv/
ENV/
backend.log
*.log
.DS_Store
EOF
      
      git add .
      git commit -m "Initial commit"
      echo "✅ Git repository initialized"
    fi
    
    echo ""
    echo "Next steps:"
    echo "1. Create a GitHub repository"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/llm-judge.git"
    echo "3. Run: git branch -M main"
    echo "4. Run: git push -u origin main"
    echo "5. Then deploy to Railway/Render using 'deploy.sh railway' or 'deploy.sh render'"
    ;;

  "local")
    echo "🏠 Testing local deployment with production settings..."
    echo ""
    
    # Stop any existing instances
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    
    # Start with production settings
    source .venv/bin/activate
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    ;;

  "help"|*)
    echo "Usage: ./deploy.sh [platform]"
    echo ""
    echo "Available platforms:"
    echo "  railway    - Deploy to Railway (easiest, $5/month)"
    echo "  render     - Deploy to Render (free tier available)"
    echo "  fly        - Deploy to Fly.io (~$3/month)"
    echo "  vercel     - Deploy frontend to Vercel (free)"
    echo "  docker     - Build and run with Docker locally"
    echo "  github     - Initialize git and push to GitHub"
    echo "  local      - Test production build locally"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh railway    # Get Railway deployment instructions"
    echo "  ./deploy.sh fly        # Deploy to Fly.io"
    echo "  ./deploy.sh vercel     # Deploy frontend to Vercel"
    echo ""
    echo "📚 For detailed guides, see DEPLOYMENT.md"
    ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Need help? Check DEPLOYMENT.md for detailed guides!"
