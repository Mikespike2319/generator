@echo off
echo Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Creating virtual environment...
if not exist venv (
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Installing package in development mode...
pip install -e .

echo Running application...
cd src
python main.py

echo Deactivating virtual environment...
call ..\venv\Scripts\deactivate.bat

pause 