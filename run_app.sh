#!/bin/bash
# Script to run the Streamlit app locally (no Docker required!)

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found!"
    echo "Run './setup_local.sh' first to set up your development environment."
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
echo "🚀 Starting Streamlit app..."
echo "📖 The app will open at http://localhost:8501"
echo ""
streamlit run app.py

