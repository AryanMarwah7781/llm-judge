# Branch Structure

## Overview

This repository uses a feature branch workflow with the following branches:

---

## Main Branch

**Branch:** `main`  
**Status:** ✅ Production-ready  
**Remote:** `origin/main`  
**Latest Commit:** 246849d - docs: Add comprehensive technical blog post (SUMMARY.md)

### Recent Commits (Latest 5)
- `246849d` - docs: Add comprehensive technical blog post (SUMMARY.md)
- `24dc4a6` - docs: Add deployment status, features guide, and testing script
- `050928d` - fix: Complete frontend integration for templates and safety warnings
- `f9219c9` - Add frontend support for templates and safety warnings
- `14af112` - Add custom criteria templates and lightweight safety checks

### Deployed To
- **Backend:** https://web-production-446a5.up.railway.app (Railway)
- **Frontend:** https://llm-judge.vercel.app (Vercel)

### Features
- Complete LLM evaluation system
- Multi-model support (GPT-4o, Claude Sonnet 4, GPT-4o Mini)
- Custom criteria templates
- Lightweight safety checks (bias + adversarial detection)
- Template management (save/load/CRUD)
- Comprehensive documentation

---

## Feature Branches

### 1. feature/templates-and-safety

**Status:** ✅ Merged to main  
**Remote:** `origin/feature/templates-and-safety`  
**Latest Commit:** f9219c9 - Add frontend support for templates and safety warnings

**Purpose:**  
Development branch for custom criteria templates and lightweight safety features.

**Key Commits:**
- `f9219c9` - Add frontend support for templates and safety warnings
- `14af112` - Add custom criteria templates and lightweight safety checks

**Features Added:**
- Template CRUD API (`/api/templates`)
- Template storage (JSON-based)
- Domain-specific template filtering
- Adversarial detection (jailbreak, prompt injection, sycophancy)
- Bias detection (gender, age, racial, socioeconomic, ability)
- Safety warnings in evaluation responses
- Frontend template save/load UI
- Safety warnings display (yellow alert boxes)

**Status:** ✅ Successfully merged to main via commit 050928d

---

### 2. feature/groundbreaking-ai-safety

**Status:** 🔬 Research branch  
**Remote:** `origin/feature/groundbreaking-ai-safety`  
**Latest Commit:** 2e8097c - Update gitignore

**Purpose:**  
Experimental branch for advanced AI safety research features.

**Key Commits:**
- `2e8097c` - Update gitignore
- `d68f661` - Notebook updated
- `7126d5a` - refactor: Clean up documentation and rename files
- `8f7fac4` - Final notebook state
- `2593f7d` - setup: Create clean llmjudgevenv virtual environment

**Research Components:**
1. **Adversarial Detection Module**
   - Jailbreak detection
   - Many-shot attack detection
   - Prompt injection patterns

2. **Bias Testing Framework**
   - Multi-category bias detection
   - Pattern-based analysis
   - Statistical scoring

3. **Robustness Testing**
   - Model consistency checks
   - Adversarial examples testing

4. **Research Notebooks**
   - Interactive Jupyter notebooks
   - Demonstrations of safety features
   - Performance benchmarks

**Additional Dependencies:**
- `torch==2.1.0` - Deep learning framework
- `transformers==4.36.0` - HuggingFace models
- `numpy==1.24.3` - Numerical computations
- `rich==13.7.0` - Pretty console output
- `plotly==5.18.0` - Interactive visualizations
- `pandas==2.1.4` - Data analysis

**Note:** This branch contains research code and is NOT deployed to production. Core safety features were extracted and integrated into main via the `feature/templates-and-safety` branch.

---

## Branch Workflow

```
main (production)
  │
  ├─── feature/templates-and-safety (merged)
  │      ├─ Template CRUD API
  │      ├─ Safety checks integration
  │      └─ Frontend UI updates
  │      
  └─── feature/groundbreaking-ai-safety (research)
         ├─ Advanced safety research
         ├─ Research notebooks
         └─ Experimental features
```

---

## Branch Management

### Creating a New Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name main

# Make changes and commit
git add .
git commit -m "feat: Your feature description"

# Push to remote
git push -u origin feature/your-feature-name
```

### Merging to Main

```bash
# Switch to main and update
git checkout main
git pull origin main

# Merge feature branch (fast-forward)
git merge feature/your-feature-name

# Push to remote
git push origin main
```

### Keeping Feature Branch Updated

```bash
# Switch to feature branch
git checkout feature/your-feature-name

# Rebase on latest main
git fetch origin
git rebase origin/main

# Push updates (force if rebased)
git push origin feature/your-feature-name
```

---

## Remote Repository

**GitHub:** https://github.com/AryanMarwah7781/llm-judge

### All Branches on Remote
- `origin/main` ✅
- `origin/feature/templates-and-safety` ✅
- `origin/feature/groundbreaking-ai-safety` ✅

### Branch Protection Rules (Recommended)

For `main` branch:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Include administrators in restrictions

---

## Deployment Triggers

**Railway (Backend):**
- Triggers on push to `main` branch
- Auto-deploys within 2-3 minutes
- Health check at: `/api/health`

**Vercel (Frontend):**
- Triggers on push to `main` branch
- Auto-deploys within 1-2 minutes
- Preview deployments for PRs

---

## Branch Cleanup

### After Successful Merge

```bash
# Delete local branch
git branch -d feature/your-feature-name

# Delete remote branch
git push origin --delete feature/your-feature-name
```

**Note:** Keep research branches (`feature/groundbreaking-ai-safety`) for reference and future development.

---

## Summary

| Branch | Status | Remote | Purpose | Deployed |
|--------|--------|--------|---------|----------|
| `main` | ✅ Active | ✅ Synced | Production | ✅ Yes |
| `feature/templates-and-safety` | ✅ Merged | ✅ Synced | Templates + Safety | ✅ Yes (in main) |
| `feature/groundbreaking-ai-safety` | 🔬 Research | ✅ Synced | Advanced Research | ❌ No |

---

**All branches successfully pushed to GitHub!** 🎉

**Repository URL:** https://github.com/AryanMarwah7781/llm-judge  
**Last Updated:** October 21, 2025
