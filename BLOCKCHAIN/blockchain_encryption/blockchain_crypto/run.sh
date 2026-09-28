#!/bin/bash

# BlockChain File Encryption - macOS/Linux Launcher

echo ""
echo "============================================"
echo "  BlockChain File Encryption System"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    echo "Install using: brew install python3 (macOS) or apt-get install python3 (Linux)"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Using Python $python_version"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "============================================"
echo "  Starting BlockChain File Encryption"
echo "============================================"
echo ""
echo "Opening http://localhost:5000 in your browser..."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser
sleep 2
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5000
else
    xdg-open http://localhost:5000 2>/dev/null || echo "Please open http://localhost:5000 in your browser"
fi

# Run Flask app
python3 app.py
