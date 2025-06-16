@echo off
title Excel Data Analysis Report Generator - Installer
color 0A

echo.
echo ===============================================
echo  Excel Data Analysis Report Generator
echo  Windows Installation Script
echo ===============================================
echo.

REM Check for Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://python.org/downloads/
    echo.
    echo ⚠️  IMPORTANT: During installation, make sure to:
    echo    ✅ Check "Add Python to PATH"
    echo    ✅ Check "Install for all users" (recommended)
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python found!

REM Check if virtual environment already exists
echo.
echo [2/5] Setting up virtual environment...
if exist venv (
    echo ⚠️  Virtual environment already exists. Removing old version...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created!

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo.
echo [5/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo.
    echo Try running this command manually:
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ All dependencies installed successfully!

REM Create desktop shortcut (optional)
echo.
set /p create_shortcut="Create desktop shortcut? (y/n): "
if /i "%create_shortcut%"=="y" (
    echo Creating desktop shortcut...
    set "current_dir=%cd%"
    echo @echo off > "%USERPROFILE%\Desktop\Excel Report Generator.bat"
    echo cd /d "%current_dir%" >> "%USERPROFILE%\Desktop\Excel Report Generator.bat"
    echo call run.bat >> "%USERPROFILE%\Desktop\Excel Report Generator.bat"
    echo ✅ Desktop shortcut created!
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo ===============================================
echo  🎉 Installation Complete!
echo ===============================================
echo.
echo To run the application:
echo   • Double-click "run.bat" in this folder
if /i "%create_shortcut%"=="y" (
echo   • Or use the desktop shortcut
)
echo.
echo The application will:
echo   ✅ Load Excel files (.xlsx, .xls)
echo   ✅ Analyze your data automatically
echo   ✅ Generate professional HTML reports
echo   ✅ Open reports in your browser
echo.
set /p run_now="Run the application now? (y/n): "
if /i "%run_now%"=="y" (
    echo.
    echo Starting application...
    call run.bat
) else (
    echo.
    echo You can run the application anytime by double-clicking "run.bat"
    pause
) 