#!/bin/bash

# E-Commerce Price Predictor - Startup Script
# This script sets up and runs the web application

echo "🛒 E-Commerce Price Predictor - Web Application"
echo "================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements_web.txt -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for required files
echo ""
echo "🔍 Checking required files..."

required_files=(
    "simple_models/best_model.pth"
    "Transformer_Ready_Input/transform_info.pkl"
    "Transformer_Ready_Input/feature_prep.pkl"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "⚠️  Some required files are missing."
    echo "Please ensure you have:"
    echo "  1. Trained model: simple_models/best_model.pth"
    echo "  2. Preprocessors: Transformer_Ready_Input/*.pkl"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the application
echo ""
echo "🚀 Starting Flask application..."
echo ""
echo "================================================"
echo "   Application will be available at:"
echo "   http://localhost:5000"
echo ""
echo "   Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Run Flask app
python3 app.py
