# 🚀 Quick Deploy Guide

## Fastest Way to Deploy (5 minutes)

### Option 1: Railway (Recommended - $5/month)

1. **Push to GitHub:**
```bash
./deploy.sh github
# Follow the instructions to push to GitHub
```

2. **Deploy:**
- Go to [railway.app](https://railway.app)
- Click "Start a New Project" → "Deploy from GitHub repo"
- Select your repository
- Add environment variables:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
- Done! You get a URL like: `https://llm-judge-production.up.railway.app`

3. **Update Frontend:**
Edit `index.html` line 115:
```javascript
const API_BASE_URL = 'https://your-app.railway.app';
```

4. **Deploy Frontend:**
```bash
./deploy.sh vercel
```

### Option 2: Render (Free)

1. **Push to GitHub** (same as above)

2. **Deploy:**
- Go to [render.com](https://render.com)
- Click "New +" → "Web Service"
- Connect your GitHub
- Render auto-detects `render.yaml`
- Add API keys
- Done! URL: `https://llm-judge.onrender.com`

⚠️ Free tier sleeps after 15min (30-60s cold start)

### Option 3: Docker (Local/Any Platform)

```bash
./deploy.sh docker
```

Opens at: http://localhost:8000

---

## 📝 Before You Deploy

1. **Make sure `.env` is NOT committed:**
```bash
git status
# Should NOT see .env in the list
```

2. **Test locally first:**
```bash
./start.sh
# Verify everything works
```

3. **Update frontend URL after backend deployment**

---

## 💰 Cost Comparison

| Platform | Cost | Cold Start | Deployment | Best For |
|----------|------|-----------|------------|----------|
| **Railway** | $5/mo | None | GitHub auto-deploy | Production |
| **Render Free** | $0 | 30-60s | GitHub auto-deploy | Testing |
| **Render Paid** | $7/mo | None | GitHub auto-deploy | Production |
| **Fly.io** | ~$3/mo | None | CLI deploy | Docker fans |
| **Vercel (Frontend)** | $0 | None | CLI/GitHub | Frontend only |

---

## 🆘 Need Help?

See `DEPLOYMENT.md` for detailed guides for each platform!

**Quick commands:**
```bash
./deploy.sh railway    # Railway guide
./deploy.sh render     # Render guide  
./deploy.sh fly        # Deploy to Fly.io
./deploy.sh vercel     # Deploy frontend
./deploy.sh docker     # Local Docker test
```
