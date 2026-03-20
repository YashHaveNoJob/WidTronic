@echo off
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

:: Install required packages if missing
echo Checking dependencies...
python -c "import pystray, PIL" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    python -m pip install --upgrade pip
    python -m pip install pystray pillow
)

:: Run the clock without a console window
start /b pythonw main.py
exit