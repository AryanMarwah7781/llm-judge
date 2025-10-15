# 🌐 Custom Domain Setup for Railway

## Quick Setup Guide

### Your Current URLs:
- **Backend (Railway):** `https://web-production-446a5.up.railway.app`
- **Frontend (Vercel):** Your Vercel URL

---

## 🎯 Recommended Domain Structure:

**Backend API:**
- `https://api.llmjudge.com` (professional)
- or `https://api.yourdomain.com`

**Frontend:**
- `https://llmjudge.com` (on Vercel)
- or `https://www.llmjudge.com`

---

## 📋 Step-by-Step Instructions:

### **1. Buy a Domain (if you don't have one)**

Recommended providers:
- **Namecheap:** ~$10/year (cheap, reliable)
- **GoDaddy:** ~$12/year (popular)
- **Google Domains:** ~$12/year (simple)
- **Cloudflare:** ~$10/year (best for developers)

Suggested names:
- `llmjudge.com`
- `llm-judge.com`
- `judgeai.com`
- `evalai.com`

---

### **2. Add Domain to Railway**

1. Go to Railway dashboard
2. Click your service
3. Settings → Networking
4. Click "Custom Domain"
5. Enter: `api.yourdomain.com`
6. Railway shows you: `i52s65g5.up.railway.app`

---

### **3. Configure DNS**

**Go to your domain provider and add:**

```
Type:  CNAME
Name:  api
Value: i52s65g5.up.railway.app
TTL:   3600 (or Auto)
```

**Example for different providers:**

#### Cloudflare (Recommended):
```
Dashboard → Domain → DNS → Add Record
Type: CNAME
Name: api
Target: i52s65g5.up.railway.app
Proxy: OFF (gray cloud)
```

#### Namecheap:
```
Domain List → Manage → Advanced DNS
Add New Record:
Type: CNAME Record
Host: api
Value: i52s65g5.up.railway.app
```

#### GoDaddy:
```
My Products → DNS
Add → Type: CNAME
Name: api
Value: i52s65g5.up.railway.app
```

---

### **4. Wait for DNS Propagation**

**Check status:**
```bash
# In terminal
nslookup api.yourdomain.com

# Should show:
# api.yourdomain.com  canonical name = i52s65g5.up.railway.app
```

**Or use online checker:**
- https://dnschecker.org

**Typical wait time:** 5-15 minutes

---

### **5. Verify SSL Certificate**

Once DNS propagates:
1. Railway auto-detects the CNAME
2. Shows ✅ "Record detected"
3. Provisions SSL certificate (1-2 min)
4. Your API is live at `https://api.yourdomain.com`

**Test it:**
```bash
curl https://api.yourdomain.com/api/health
```

---

### **6. Update Frontend**

After custom domain is working, update `index.html`:

**Change this line (around line 100):**
```javascript
const API_BASE_URL = 'https://web-production-446a5.up.railway.app';
```

**To:**
```javascript
const API_BASE_URL = 'https://api.yourdomain.com';
```

**Then commit and push:**
```bash
git add index.html
git commit -m "Update API URL to custom domain"
git push origin main
```

Vercel will auto-deploy with the new URL!

---

### **7. Add Frontend Domain to Vercel**

1. Go to Vercel dashboard
2. Select your project
3. Settings → Domains
4. Add domain: `yourdomain.com`
5. Vercel gives you DNS instructions
6. Add to your DNS provider:
   ```
   Type: CNAME
   Name: @ (or www)
   Value: cname.vercel-dns.com
   ```

---

## 🎯 Final Result:

```
Backend API:  https://api.yourdomain.com
Frontend:     https://yourdomain.com
GitHub:       https://github.com/AryanMarwah7781/llm-judge
```

**Example request:**
```bash
curl -X POST https://api.yourdomain.com/api/evaluate \
  -F "file=@questions.pdf" \
  -F 'criteria=[{"name":"ACCURACY","weight":100}]' \
  -F "judge_model=gpt-4o-mini"
```

---

## 🔒 Security Notes:

✅ Railway auto-provisions **SSL/TLS certificate** (HTTPS)
✅ Certificate auto-renews (Let's Encrypt)
✅ No additional configuration needed
✅ Vercel also provides automatic HTTPS

---

## 🐛 Troubleshooting:

### **DNS not propagating:**
- Wait 15-30 minutes
- Clear your DNS cache: `sudo dscacheutil -flushcache` (Mac)
- Check with: `nslookup api.yourdomain.com`

### **Railway shows "Record not detected":**
- Verify CNAME value is exact: `i52s65g5.up.railway.app`
- Check DNS provider for typos
- Wait 5-10 more minutes

### **SSL certificate not working:**
- Railway provisions after DNS detection
- Wait 1-2 minutes after "Record detected"
- Check https://api.yourdomain.com/api/health

### **Frontend can't connect:**
- Update API_BASE_URL in index.html
- Push to GitHub (Vercel auto-deploys)
- Clear browser cache

---

## 💰 Costs:

- **Domain:** ~$10-15/year
- **Railway:** $5/month (same)
- **Vercel:** Free (same)
- **SSL:** Free (automatic)

**Total change:** +$10-15/year for domain

---

## 📝 DNS Record Summary:

**For backend (Railway):**
```
api.yourdomain.com → CNAME → i52s65g5.up.railway.app
```

**For frontend (Vercel):**
```
yourdomain.com → CNAME → cname.vercel-dns.com
```

---

## 🎉 Benefits of Custom Domain:

✅ Professional appearance
✅ Brand recognition
✅ Easier to remember
✅ Better for production
✅ Custom email addresses (bonus!)

---

## ⏭️ Next Steps:

1. **Choose & buy domain** (~5 minutes)
2. **Add to Railway** (2 minutes)
3. **Configure DNS** (5 minutes)
4. **Wait for propagation** (5-30 minutes)
5. **Verify & update frontend** (2 minutes)

**Total time:** ~30 minutes (mostly waiting)

---

**Need help with any step? Just ask!** 🚀
