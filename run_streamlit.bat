@echo off
REM AXIS AI Streamlit Launcher for Windows
echo ========================================
echo   AXIS AI - Streamlit Web Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Streamlit not found. Installing dependencies...
    pip install -r requirements_streamlit.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please create a .env file with your API keys.
    echo.
    pause
)

REM Create necessary directories
if not exist Data mkdir Data
if not exist Frontend\Files mkdir Frontend\Files

REM Run Streamlit
echo [INFO] Starting Streamlit...
echo [INFO] The app will open in your default browser
echo [INFO] Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause

