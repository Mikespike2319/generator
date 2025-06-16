@echo off
echo Starting Hospital Report Generator...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist "venv\Lib\site-packages\customtkinter" (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Run the application
python src/main.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat 