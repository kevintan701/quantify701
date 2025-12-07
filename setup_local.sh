#!/bin/bash
# Quick setup script for local development (no Docker required)

echo "🚀 Setting up local development environment..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the app, use one of these commands:"
echo "  ./run_app.sh"
echo "  OR"
echo "  source venv/bin/activate && streamlit run app.py"
echo ""
echo "The app will open at http://localhost:8501"
echo ""
echo "💡 Remember: You don't need Docker for local development!"

