@echo off
REM Quick Start Script for Sales Analytics Dashboard (Windows)

echo ==========================================
echo   Sales Analytics Dashboard
echo   Quick Start Script - Windows
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo. Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Check for .env file
if not exist ".env" (
    echo Warning: No .env file found
    echo The app will run with sample data
    echo.
    echo To use Supabase (optional^):
    echo   1. Copy .env.example to .env
    echo   2. Add your Supabase credentials
    echo.
) else (
    echo .env file found
)

echo.

REM Run verification
echo Running verification checks...
python verify_setup.py

echo.
echo ==========================================
echo Starting Streamlit Dashboard...
echo ==========================================
echo.
echo The dashboard will open in your browser at:
echo   http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
streamlit run app.py
