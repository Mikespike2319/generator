@echo off
echo Setting up Hospital Report Generator...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements first
echo Installing requirements...
pip install -r requirements.txt

REM Install the package in development mode
echo Installing package in development mode...
pip install -e .

REM Run the application
echo Starting Hospital Report Generator...
python -m hospital_report_generator

REM Deactivate virtual environment
call venv\Scripts\deactivate

pause 