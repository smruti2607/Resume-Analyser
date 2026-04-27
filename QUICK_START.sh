#!/bin/bash
# 🚀 AI Resume Analyzer - Quick Start Script
# Run this script to set up and start the application

set -e  # Exit on error

echo "🚀 AI Resume Analyzer - Quick Start Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version found"
echo ""

# Check for .env file
echo "Checking configuration..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created. Please edit it with your OpenAI API key!"
        echo ""
        echo "1. Get your key from: https://platform.openai.com/api-keys"
        echo "2. Edit .env and replace: sk_your_key_here_paste_your_actual_key"
        echo "3. Run this script again"
        exit 1
    fi
else
    echo "✅ .env file found"
fi

# Check for OpenAI API key
if grep -q "your_key_here\|sk_" .env; then
    echo "⚠️  OpenAI API key not configured in .env"
    echo "Get it from: https://platform.openai.com/api-keys"
    exit 1
else
    echo "✅ OpenAI API key configured"
fi
echo ""

# Setup Backend
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend setup complete"
cd ..
echo ""

# Setup Frontend
echo "Setting up frontend..."
cd frontend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "✅ Frontend setup complete"
cd ..
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 Start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "  python -m uvicorn main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "  streamlit run app.py"
echo ""
echo "Then open: http://localhost:8501"
echo ""
