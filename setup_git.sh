#!/bin/bash
# Script to set up Git repository for Streamlit Cloud deployment

echo "🚀 Setting up Git repository for Quantify app..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
else
    echo "✓ Git repository already initialized"
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "none")

if [ "$CURRENT_BRANCH" = "master" ]; then
    echo "🔄 Renaming branch from 'master' to 'main'..."
    git branch -M main
    CURRENT_BRANCH="main"
elif [ "$CURRENT_BRANCH" = "none" ]; then
    echo "📝 Creating initial commit on 'main' branch..."
    git checkout -b main
    CURRENT_BRANCH="main"
fi

echo "✓ Current branch: $CURRENT_BRANCH"

# Add all files
echo "📁 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit (everything is already committed)"
else
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Quantify - AI-Powered Quantitative Investment Platform by The Studio 701 LLC"
fi

echo ""
echo "✅ Git repository is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Create a repository on GitHub (name it 'quantify' or your preferred name)"
echo "2. Run these commands (replace with your GitHub URL):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/quantify.git"
echo "   git push -u origin main"
echo ""
echo "3. Go to https://share.streamlit.io and deploy your app"
echo "   - Repository: YOUR_USERNAME/quantify"
echo "   - Branch: main"
echo "   - Main file path: app.py"
echo ""

