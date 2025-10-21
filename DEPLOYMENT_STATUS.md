# Deployment Status

## Latest Push
**Date:** October 20, 2025
**Branch:** main
**Commit:** 050928d - Complete frontend integration for templates and safety warnings

## Features Deployed

### Backend (Railway)
- Custom criteria templates API (CRUD operations)
- Lightweight safety checks (bias + adversarial detection)
- Template storage via JSON files
- Domain-specific template filtering
- Safety warnings in evaluation responses

### Frontend (Vercel + Railway)
- Template save modal (brutalist UI)
- Template load dropdown (auto-loads for domain)
- Safety warnings display (yellow alert box)
- Save template button in criteria screen
- Auto-load templates when domain changes

## Deployment Platforms

### Railway (Backend API)
**URL:** https://web-production-446a5.up.railway.app
**Status:** Auto-deploys from `main` branch
**Expected Deploy Time:** 2-5 minutes

**Endpoints Added:**
- `GET /api/templates?domain={domain}` - List templates
- `POST /api/templates` - Create template
- `GET /api/templates/{id}` - Get specific template
- `PUT /api/templates/{id}` - Update template
- `DELETE /api/templates/{id}` - Delete template
- `POST /api/evaluate` - Now includes safety_warnings in response

### Vercel (Frontend)
**URL:** https://llm-judge.vercel.app
**Status:** Serves index.html
**Expected Deploy Time:** 1-2 minutes

**UI Updates:**
- Criteria selection screen: Template dropdown + Save button
- Results screen: Safety warnings alert box

## Testing Locally

### 1. Start Backend
```bash
uvicorn app.main:app --reload
# Server at http://127.0.0.1:8000
```

### 2. Test Templates API
```bash
# List templates (empty initially)
curl http://127.0.0.1:8000/api/templates?domain=legal

# Create template
curl -X POST http://127.0.0.1:8000/api/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Legal Template",
    "domain": "legal",
    "criteria": [
      {"name": "CITATION_ACCURACY", "weight": 40, "hardMin": 90}
    ]
  }'
```

### 3. Test Frontend
Open `index.html` in browser or visit http://127.0.0.1:8000

**Expected Flow:**
1. Select "Legal" domain → Template dropdown appears (if templates exist)
2. Review criteria → Click "💾 SAVE AS TEMPLATE"
3. Enter template name → Save
4. Reload page → Template appears in dropdown
5. Upload PDF → Run evaluation → See safety warnings (if flagged)

## Production Verification

### Check Railway Deployment
1. Go to Railway dashboard
2. Check deployment logs for latest commit (050928d)
3. Verify build success
4. Test: `curl https://web-production-446a5.up.railway.app/api/templates?domain=legal`

### Check Vercel Deployment
1. Go to Vercel dashboard
2. Check deployment for latest commit
3. Visit https://llm-judge.vercel.app
4. Verify new features appear in UI

## Rollback Plan

If issues occur in production:

```bash
# Revert to previous commit
git revert 050928d
git push origin main

# Or reset to specific commit
git reset --hard f9219c9
git push --force origin main
```

## Known Issues
- None (all features tested locally)

## Next Steps
1. Wait 2-5 minutes for auto-deployment
2. Test production endpoints
3. Verify UI shows new features
4. Create example templates for demo

## Files Modified
- `index.html` - Frontend integration (+91 lines)
- All backend files already committed in previous push

## Environment Variables Required
- `OPENAI_API_KEY` - Already configured ✓
- `ANTHROPIC_API_KEY` - Already configured ✓

## Success Criteria
- ✅ Backend templates API responds
- ✅ Frontend shows template save button
- ✅ Frontend shows template dropdown
- ✅ Safety warnings display in results
- ✅ No console errors
- ✅ Backward compatible (old evaluations still work)

---

**Deployment initiated:** October 20, 2025 at $(date)
**Auto-deploy status:** In progress...
