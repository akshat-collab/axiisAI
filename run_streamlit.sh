#!/bin/bash
# AXIS AI Streamlit Launcher for macOS/Linux

echo "========================================"
echo "  AXIS AI - Streamlit Web Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Check if streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "[INFO] Streamlit not found. Installing dependencies..."
    pip3 install -r requirements_streamlit.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create a .env file with your API keys."
    echo ""
    read -p "Press Enter to continue..."
fi

# Create necessary directories
mkdir -p Data
mkdir -p Frontend/Files

# Run Streamlit
echo "[INFO] Starting Streamlit..."
echo "[INFO] The app will open in your default browser"
echo "[INFO] Press Ctrl+C to stop the server"
echo ""
python3 -m streamlit run app.py

