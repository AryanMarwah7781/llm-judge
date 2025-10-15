# 🚂 Railway Deployment Guide

## 🎯 Deploy Your LLM Judge Platform to Railway in 5 Minutes

Railway is the perfect choice for your app - simple, professional, and always-on with no cold starts!

---

## 📋 Prerequisites

✅ Your code is already on GitHub: `AryanMarwah7781/llm-judge`  
✅ You have your API keys ready  
✅ Railway configuration files are ready (`railway.json`, `Procfile`)

---

## 🚀 Step-by-Step Deployment

### **Step 1: Create Railway Account**

1. Go to **https://railway.app**
2. Click **"Login"** (top right)
3. Select **"Login with GitHub"**
4. Authorize Railway to access your GitHub account

💡 **Why GitHub login?** Makes deployment super easy - one-click connection to your repo!

---

### **Step 2: Create New Project**

1. Once logged in, click **"New Project"** (or **"Start a New Project"**)
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repositories
4. Find and select **`llm-judge`**
5. Railway will automatically detect it's a Python app!

**What Railway does automatically:**
- ✅ Detects Python from `requirements.txt`
- ✅ Uses `Procfile` for start command
- ✅ Installs dependencies
- ✅ Assigns a PORT
- ✅ Generates a public URL

---

### **Step 3: Add Environment Variables**

🔐 **CRITICAL:** Add your API keys in Railway (never commit them to git!)

1. In Railway dashboard, click on your **deployed service**
2. Go to the **"Variables"** tab
3. Click **"+ New Variable"** and add these:

```bash
# Required - Add your actual keys here
OPENAI_API_KEY=sk-proj-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Optional - Recommended settings
ENVIRONMENT=production
LOG_LEVEL=INFO
GLOBAL_THRESHOLD=85
MAX_RETRIES=3
RETRY_DELAY=1

# CORS - Allow your frontend domain
ALLOWED_ORIGINS=*
```

💡 **Pro tip:** Railway automatically injects a `PORT` variable, so you don't need to set it!

---

### **Step 4: Deploy!**

Railway deploys automatically after adding variables!

1. Watch the **"Deployments"** tab
2. You'll see:
   ```
   Building...
   Installing dependencies...
   Starting uvicorn...
   ✅ Deployment successful!
   ```
3. This takes **2-3 minutes** the first time

---

### **Step 5: Get Your Public URL**

1. In the **"Settings"** tab, scroll to **"Networking"**
2. Click **"Generate Domain"**
3. Railway gives you a URL like:
   ```
   https://llm-judge-production.up.railway.app
   ```
4. **Test it!** Open in browser:
   ```
   https://your-app.railway.app/api/health
   ```

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T...",
  "environment": "production"
}
```

🎉 **Your backend is LIVE!**

---

## 🔧 Post-Deployment Configuration

### **Test Your API**

```bash
# Health check
curl https://your-app.railway.app/api/health

# Test evaluation (replace with your URL)
curl -X POST https://your-app.railway.app/api/evaluate \
  -F "file=@law_questions.pdf" \
  -F 'criteria=[{"name":"CITATION_ACCURACY","weight":100,"hardMin":80,"description":"Check citations"}]' \
  -F "judge_model=gpt-4o-mini"
```

### **Enable Auto-Deploy from GitHub**

Railway does this automatically! Every time you push to `main`:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway will automatically:
1. Detect the push
2. Build the new version
3. Deploy it
4. Zero-downtime rollout!

---

## 🎨 Deploy Frontend to Vercel

Now let's deploy your frontend so it's accessible on the web:

### **Step 1: Update Frontend API URL**

First, update your frontend to use the Railway backend URL:

1. Open `index.html`
2. Find this line (around line 15):
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```
3. Change it to your Railway URL:
   ```javascript
   const API_BASE_URL = 'https://your-app.railway.app';
   ```
4. Save and commit:
   ```bash
   git add index.html
   git commit -m "Update API URL for production"
   git push origin main
   ```

### **Step 2: Deploy to Vercel**

1. Go to **https://vercel.com**
2. Click **"Add New..." → "Project"**
3. Import **`llm-judge`** from GitHub
4. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (leave empty)
   - **Output Directory:** `./`
5. Click **"Deploy"**

Vercel will give you a URL like:
```
https://llm-judge.vercel.app
```

🎉 **Your frontend is LIVE!**

---

## 💰 Costs & Billing

### **Railway Pricing:**

**Trial (First 500 hours):**
- FREE for the first 500 hours (~20 days of 24/7 uptime)
- Perfect for testing!

**After Trial:**
- **$5/month** flat rate
- Includes:
  - 500 hours of runtime
  - 100GB bandwidth
  - 1GB memory
  - 1 vCPU

**Usage-based:**
- Additional hours: $0.01/hour
- Additional bandwidth: $0.10/GB

**Your estimated cost:** ~$5-7/month

### **Total Monthly Cost:**
- Railway (Backend): **$5/month**
- Vercel (Frontend): **$0** (free tier)
- OpenAI API (1000 evals with GPT-4o-mini): **$2**
- **Total: ~$7/month** 💰

---

## 📊 Monitoring & Logs

### **View Logs in Railway:**

1. Click on your service
2. Go to **"Deployments"** tab
3. Click **"View Logs"**

You'll see real-time logs:
```
INFO:     Uvicorn running on http://0.0.0.0:8080
INFO:     Application startup complete
INFO:     POST /api/evaluate - 200 OK
```

### **Monitor Usage:**

1. Go to **"Metrics"** tab
2. See:
   - CPU usage
   - Memory usage
   - Network traffic
   - Response times

### **Set Up Alerts:**

1. Go to **"Settings" → "Webhooks"**
2. Add Slack/Discord/Email notifications for:
   - Deployment failures
   - High CPU/memory usage
   - Errors

---

## 🔐 Security Best Practices

### ✅ **Already Done:**
- [x] API keys in environment variables (not in code)
- [x] `.env` in `.gitignore`
- [x] HTTPS enabled automatically by Railway
- [x] CORS configured in `app/main.py`

### 🔒 **Additional Security (Optional):**

**1. Add API Authentication:**
Update `app/main.py` to require an API key:

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("FRONTEND_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Then add to Railway variables:
```
FRONTEND_API_KEY=your-secret-key-here
```

**2. Rate Limiting (Already Built-in!):**
Your app already has rate limiting in `app/main.py`:
- Max 3 retries
- Exponential backoff

**3. Domain with SSL:**
Add a custom domain in Railway:
1. Go to **"Settings" → "Domains"**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Update your DNS records
5. Railway automatically provisions SSL!

---

## 🚀 Advanced Features

### **1. Add Database (PostgreSQL):**

```bash
# In Railway dashboard
Click "New" → "Database" → "Add PostgreSQL"
```

Railway automatically:
- Creates a PostgreSQL instance
- Injects `DATABASE_URL` environment variable
- Handles backups

### **2. Enable Redis (Caching):**

```bash
# In Railway dashboard
Click "New" → "Database" → "Add Redis"
```

Use for caching LLM responses:
```python
import redis
cache = redis.from_url(os.getenv("REDIS_URL"))
```

### **3. Multiple Environments:**

Create separate projects:
- `llm-judge-production` (main branch)
- `llm-judge-staging` (develop branch)

---

## 🐛 Troubleshooting

### **Deployment Failed:**

**Check logs:**
1. Go to "Deployments" → "View Logs"
2. Look for error messages

**Common issues:**
- Missing environment variable → Add in "Variables" tab
- Wrong Python version → Add `runtime.txt` with `python-3.11`
- Port binding error → Railway auto-sets PORT, don't hardcode 8000

### **API Not Responding:**

**Check health endpoint:**
```bash
curl https://your-app.railway.app/api/health
```

**Check service status:**
1. Railway dashboard → "Metrics"
2. Ensure service is running (green dot)

**Restart service:**
1. Go to "Settings"
2. Click "Restart"

### **High Costs:**

**Monitor usage:**
1. Check "Usage" tab in Railway
2. Look for:
   - Unexpected traffic spikes
   - Memory leaks
   - Long-running requests

**Optimize:**
```python
# Add request timeouts
from fastapi import Request
import asyncio

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=30.0)
    except asyncio.TimeoutError:
        return JSONResponse({"error": "Request timeout"}, status_code=504)
```

---

## 📝 Helpful Commands

### **View Logs from CLI:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs
```

### **Deploy from CLI:**
```bash
railway up
```

### **Open Dashboard:**
```bash
railway open
```

---

## ✅ Deployment Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Environment variables added (API keys)
- [ ] Public URL generated
- [ ] Health endpoint tested
- [ ] Frontend deployed to Vercel
- [ ] Frontend updated with Railway API URL
- [ ] API evaluation tested end-to-end
- [ ] Logs checked for errors
- [ ] CORS configured for frontend domain
- [ ] Monitoring/alerts set up (optional)

---

## 🎉 You're Live!

Your LLM Judge Platform is now deployed and ready for production use!

**Your URLs:**
- **Backend API:** `https://your-app.railway.app`
- **Frontend:** `https://llm-judge.vercel.app`
- **Health Check:** `https://your-app.railway.app/api/health`

**Share your API:**
```bash
# Example usage
curl -X POST https://your-app.railway.app/api/evaluate \
  -F "file=@questions.pdf" \
  -F 'criteria=[{"name":"ACCURACY","weight":100,"hardMin":80}]' \
  -F "judge_model=gpt-4o-mini"
```

---

## 🤝 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Your Project Issues:** https://github.com/AryanMarwah7781/llm-judge/issues

---

## 🔄 Next Steps

1. **Monitor your first week** - Check logs and costs
2. **Add analytics** - Track API usage
3. **Set up CI/CD** - Automated testing before deploy
4. **Add features** - Build on your foundation!

**Ready to deploy? Let's do this!** 🚀
