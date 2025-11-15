#!/bin/bash

# Quick Start Script for Sales Analytics Dashboard
# This script sets up and runs the dashboard with minimal effort

echo "=========================================="
echo "  Sales Analytics Dashboard"
echo "  Quick Start Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "ℹ️  The app will run with sample data"
    echo ""
    echo "To use Supabase (optional):"
    echo "  1. Copy .env.example to .env"
    echo "  2. Add your Supabase credentials"
    echo ""
else
    echo "✅ .env file found"
fi

echo ""

# Run verification
echo "🔍 Running verification checks..."
python3 verify_setup.py

echo ""
echo "=========================================="
echo "🚀 Starting Streamlit Dashboard..."
echo "=========================================="
echo ""
echo "The dashboard will open in your browser at:"
echo "  👉 http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run app.py
