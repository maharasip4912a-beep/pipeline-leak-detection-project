#!/bin/bash

# ============================================================
# Pipeline Leak Detection Dashboard - Startup Script
# ============================================================

echo "🔍 Pipeline Leak Detection System - Dashboard Launcher"
echo "======================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⏳ Installing Streamlit..."
    pip install streamlit --quiet
    if [ $? -eq 0 ]; then
        echo "✅ Streamlit installed successfully"
    else
        echo "❌ Failed to install Streamlit"
        echo "   Try manually: pip install streamlit"
        exit 1
    fi
else
    echo "✅ Streamlit is already installed"
fi

# Check if model files exist
if [ ! -f "random_forest_model.pkl" ]; then
    echo "⚠️  Warning: random_forest_model.pkl not found!"
fi

if [ ! -f "scaler.pkl" ]; then
    echo "⚠️  Warning: scaler.pkl not found!"
fi

echo ""
echo "🚀 Starting Dashboard..."
echo "📊 The dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run Streamlit
streamlit run app.py
