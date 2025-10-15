# 🚀 Deployment Guide

Your LLM Judge Platform can be deployed to multiple platforms. Here are the easiest options:

---

## 🎯 Recommended: Railway (Easiest - $5/month)

Railway is the simplest deployment option with automatic GitHub integration.

### **Prerequisites:**
- GitHub account
- Railway account (railway.app)
- Your code pushed to GitHub

### **Step-by-Step:**

1. **Push your code to GitHub:**
```bash
cd /Users/aryanmarwah/Documents/LLMasjudge
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/llm-judge.git
git push -u origin main
```

2. **Deploy to Railway:**
- Go to https://railway.app
- Click "Start a New Project"
- Select "Deploy from GitHub repo"
- Choose your `llm-judge` repository
- Railway will auto-detect it's a Python app

3. **Set Environment Variables in Railway:**
Click on your project → Variables → Add:
```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
PORT=8000
```

4. **Done!** Railway gives you a URL like:
```
https://llm-judge-production.up.railway.app
```

---

## 🆓 Render (Free Tier Available)

Render offers a free tier perfect for testing.

### **Step-by-Step:**

1. **Push to GitHub** (same as above)

2. **Deploy to Render:**
- Go to https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Configure:
  - **Name:** llm-judge
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables:**
```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

4. **Done!** You get a URL like:
```
https://llm-judge.onrender.com
```

⚠️ **Note:** Free tier spins down after 15 min of inactivity (30-60s cold start)

---

## 🐳 Docker (Any Platform)

We already have `docker-compose.yml`! Deploy anywhere with Docker support.

### **Local Test:**
```bash
docker-compose up --build
```

### **Deploy to Fly.io (Recommended for Docker):**

1. **Install Fly CLI:**
```bash
brew install flyctl
```

2. **Login:**
```bash
fly auth login
```

3. **Create fly.toml:**
```bash
fly launch
```

4. **Set secrets:**
```bash
fly secrets set OPENAI_API_KEY=sk-proj-...
fly secrets set ANTHROPIC_API_KEY=sk-ant-...
```

5. **Deploy:**
```bash
fly deploy
```

---

## ☁️ AWS/GCP/Azure (Advanced)

For enterprise deployment:

### **AWS Elastic Beanstalk:**
```bash
eb init -p python-3.9 llm-judge
eb create llm-judge-env
eb setenv OPENAI_API_KEY=sk-proj-... ANTHROPIC_API_KEY=sk-ant-...
eb deploy
```

### **Google Cloud Run:**
```bash
gcloud run deploy llm-judge \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-proj-...,ANTHROPIC_API_KEY=sk-ant-...
```

---

## 📱 Frontend Deployment

Your frontend is static HTML, so it's even easier!

### **Option 1: Vercel (Recommended - Free)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /Users/aryanmarwah/Documents/LLMasjudge
vercel --prod
```

Update `index.html` to use your deployed backend URL:
```javascript
const API_BASE_URL = 'https://your-backend.railway.app';
```

### **Option 2: Netlify**
- Drag and drop `index.html` to netlify.com/drop
- Update backend URL in the file

### **Option 3: GitHub Pages**
```bash
# Create gh-pages branch
git checkout -b gh-pages
git push origin gh-pages
```
- Go to GitHub repo → Settings → Pages
- Select `gh-pages` branch
- Your site will be at: `https://YOUR_USERNAME.github.io/llm-judge`

### **Option 4: Serve with Backend**
Add static file serving to FastAPI:

```python
# app/main.py
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory=".", html=True), name="static")
```

Then your frontend is served at the same URL as backend!

---

## 🔐 Production Checklist

Before deploying to production:

### **Security:**
- [ ] Never commit `.env` to git (add to `.gitignore`)
- [ ] Use environment variables for API keys
- [ ] Enable HTTPS (automatic on Railway/Render/Vercel)
- [ ] Add rate limiting (we have this built-in)
- [ ] Consider API authentication for frontend

### **Performance:**
- [ ] Use multiple workers: `uvicorn app.main:app --workers 4`
- [ ] Enable logging: Check `backend.log`
- [ ] Monitor costs: Track API usage
- [ ] Add caching for repeated evaluations

### **Monitoring:**
- [ ] Set up error tracking (Sentry)
- [ ] Monitor API usage (LLM costs)
- [ ] Set up health check monitoring
- [ ] Create alerts for failures

---

## 🚀 Quick Deploy Script

I've created a deployment helper:

```bash
./deploy.sh railway   # Deploy to Railway
./deploy.sh render    # Deploy to Render
./deploy.sh fly       # Deploy to Fly.io
```

---

## 💰 Cost Estimates

### **Backend Hosting:**
- **Railway:** ~$5/month (500 hours free)
- **Render Free:** $0 (sleeps after 15min idle)
- **Render Paid:** $7/month
- **Fly.io:** ~$3/month (minimal usage)
- **Vercel:** Free for hobbyist

### **API Costs (per evaluation):**
- **GPT-4o-mini:** $0.002 (cheapest!)
- **GPT-4o:** $0.025
- **Claude Sonnet 4:** $0.030

### **Example Monthly Cost:**
- 1000 evaluations/month with GPT-4o-mini: $2
- Backend on Railway: $5
- Frontend on Vercel: Free
- **Total: ~$7/month**

---

## 🎯 Recommended Setup for Production

**Best bang for buck:**
1. **Backend:** Railway ($5/month)
2. **Frontend:** Vercel (Free)
3. **Judge Model:** GPT-4o-mini ($0.002/eval)
4. **Database:** Add PostgreSQL later if needed

**Free setup:**
1. **Backend:** Render Free (cold starts)
2. **Frontend:** Netlify/Vercel (Free)
3. **Judge Model:** GPT-4o-mini

---

## 📝 Which Should You Choose?

### **Choose Railway if:**
- ✅ You want the easiest deployment
- ✅ You can spend $5/month
- ✅ You need 24/7 availability
- ✅ You want auto-deploy from GitHub

### **Choose Render if:**
- ✅ You want free tier
- ✅ You don't mind cold starts
- ✅ You're testing/prototyping

### **Choose Fly.io if:**
- ✅ You want Docker-based deployment
- ✅ You need global edge deployment
- ✅ You want minimal cost (~$3/month)

### **Choose Vercel/Netlify if:**
- ✅ Frontend only
- ✅ You want CDN distribution
- ✅ Free is important

---

## 🚀 Let's Deploy Now!

Want me to help you deploy? Tell me which platform and I'll create the specific files you need!

**Quick start:**
```bash
# 1. Push to GitHub first
git init
git add .
git commit -m "Initial commit"
git push

# 2. Deploy to Railway (easiest)
# Just connect GitHub repo at railway.app

# 3. Update frontend URL
# Edit index.html: API_BASE_URL = 'https://your-app.railway.app'

# 4. Deploy frontend
vercel
```

**You'll be live in < 5 minutes!** 🎉
