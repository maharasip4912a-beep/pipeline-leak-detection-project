@echo off
REM ============================================================
REM Pipeline Leak Detection Dashboard - Startup Script (Windows)
REM ============================================================

cls
echo 🔍 Pipeline Leak Detection System - Dashboard Launcher
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python version: %PYTHON_VERSION%
echo.

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Installing Streamlit...
    pip install streamlit --quiet
    if %errorlevel% equ 0 (
        echo ✅ Streamlit installed successfully
    ) else (
        echo ❌ Failed to install Streamlit
        echo    Try manually: pip install streamlit
        pause
        exit /b 1
    )
) else (
    echo ✅ Streamlit is already installed
)

echo.
echo 🚀 Starting Dashboard...
echo 📊 The dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

REM Run Streamlit
streamlit run app.py

pause
