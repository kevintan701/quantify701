# Streamlit Cloud Deployment Setup Guide

## Quick Setup Steps

### Step 1: Initialize Git Repository (if not already done)

```bash
cd "/Users/the.lab.701/Documents/Work/The Studio 701 LLC/Project/Quant Trade"
git init
```

### Step 2: Create .gitignore (if not exists)

Make sure you have a `.gitignore` file that excludes:
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `.DS_Store` (macOS files)

### Step 3: Add All Files

```bash
git add .
```

### Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Quantify app with AI features"
```

### Step 5: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `quantify` (or your preferred name)
3. **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL (e.g., `https://github.com/kevintan701/quantify.git`)

### Step 6: Connect Local Repo to GitHub

```bash
# Add remote (replace with your actual GitHub URL)
git remote add origin https://github.com/kevintan701/quantify.git

# Check your current branch name
git branch

# If you see "master", rename it to "main" (Streamlit Cloud prefers "main")
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 7: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the form:
   - **Repository**: Select `kevintan701/quantify` (or your repo)
   - **Branch**: Select `main` (NOT "master")
   - **Main file path**: `app.py`
   - **App URL** (optional): `quantify` (or your preferred subdomain)
5. Click **"Deploy"**

### Step 8: Wait for Deployment

- Streamlit Cloud will install dependencies from `requirements.txt`
- First deployment may take 2-5 minutes
- Watch the logs for any errors

## Common Issues & Solutions

### Issue: "Branch does not exist"
**Solution**: Make sure you're using `main` branch, not `master`
```bash
git branch -M main
git push -u origin main
```

### Issue: "Main file path does not exist"
**Solution**: 
- Make sure `app.py` is in the root directory
- Check that it's committed and pushed to GitHub
- Verify the path is exactly `app.py` (not `./app.py` or `src/app.py`)

### Issue: Import errors after deployment
**Solution**: Make sure all dependencies are in `requirements.txt`
```bash
pip freeze > requirements.txt
# Then remove any local paths or venv references
```

### Issue: Module not found errors
**Solution**: Make sure all your Python files are in the root directory:
- `app.py`
- `ai_insights.py`
- `data_fetcher.py`
- `stock_selector.py`
- `trading_strategy.py`
- `config.py`

## Required Files for Deployment

Make sure these files are in your repository:

✅ `app.py` - Main application file  
✅ `requirements.txt` - Python dependencies  
✅ `ai_insights.py` - AI module  
✅ `data_fetcher.py` - Data fetching module  
✅ `stock_selector.py` - Stock selection module  
✅ `trading_strategy.py` - Trading strategy module  
✅ `config.py` - Configuration file  
✅ `.streamlit/config.toml` - Streamlit config (optional but recommended)  
✅ `README.md` - Documentation  

## File Structure for Streamlit Cloud

```
quantify/
├── app.py                    ← Main file (required)
├── requirements.txt          ← Dependencies (required)
├── ai_insights.py
├── data_fetcher.py
├── stock_selector.py
├── trading_strategy.py
├── config.py
├── .streamlit/
│   └── config.toml          ← Optional config
├── README.md
└── .gitignore
```

## After Deployment

Once deployed, your app will be available at:
`https://quantify-YOUR-APP-ID.streamlit.app`

Or if you set a custom URL:
`https://quantify.streamlit.app`

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy your app!

## Environment Variables (if needed later)

If you need to add API keys or secrets:
1. Go to your app settings on Streamlit Cloud
2. Click "Secrets"
3. Add your secrets in TOML format:
```toml
[secrets]
OPENAI_API_KEY = "your-key-here"
```

