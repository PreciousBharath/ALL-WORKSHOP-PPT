@echo off
REM BlockChain File Encryption - Windows Launcher

echo.
echo ============================================
echo   BlockChain File Encryption System
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip list | findstr Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the Flask app
echo.
echo ============================================
echo   Starting BlockChain File Encryption
echo ============================================
echo.
echo Opening http://localhost:5000 in your browser...
echo.
echo Press Ctrl+C to stop the server
echo.

timeout /t 2 /nobreak
start http://localhost:5000

python app.py

pause
