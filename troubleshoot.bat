@echo off
title Excel Report Generator - Troubleshoot
color 0E

echo.
echo ===============================================
echo  Excel Report Generator - Troubleshoot
echo ===============================================
echo.

echo [INFO] Gathering system information...
echo.

echo Current Directory:
echo %cd%
echo.

echo Script Directory:
echo %~dp0
echo.

echo Python Information:
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo.
    echo Solutions:
    echo 1. Install Python from https://python.org
    echo 2. Make sure "Add Python to PATH" is checked during installation
    echo 3. Restart Command Prompt after installation
) else (
    echo ✅ Python found
    echo Python location:
    where python
)
echo.

echo Pip Information:
pip --version 2>nul
if errorlevel 1 (
    echo ❌ Pip not found
) else (
    echo ✅ Pip found
)
echo.

echo Virtual Environment Check:
if exist venv (
    echo ✅ Virtual environment exists
    echo Virtual environment location: %cd%\venv
    if exist venv\Scripts\python.exe (
        echo ✅ Python executable found in venv
    ) else (
        echo ❌ Python executable missing in venv
    )
) else (
    echo ❌ Virtual environment not found
)
echo.

echo File Permissions Check:
echo Testing write permissions in current directory...
echo test > test_write.tmp 2>nul
if exist test_write.tmp (
    echo ✅ Write permissions OK
    del test_write.tmp
) else (
    echo ❌ No write permissions in current directory
    echo.
    echo Solutions:
    echo 1. Run from a user directory (not C:\Windows\System32)
    echo 2. Extract files to Documents or Desktop
    echo 3. Avoid running from restricted system directories
)
echo.

echo Requirements File Check:
if exist requirements.txt (
    echo ✅ requirements.txt found
    echo Contents:
    type requirements.txt
) else (
    echo ❌ requirements.txt not found
    echo Make sure you're in the correct directory
)
echo.

echo Network Connectivity Check:
ping -n 1 pypi.org >nul 2>&1
if errorlevel 1 (
    echo ❌ Cannot reach PyPI (package repository)
    echo Check your internet connection
) else (
    echo ✅ Network connectivity OK
)
echo.

echo ===============================================
echo  Recommended Solutions:
echo ===============================================
echo.
echo If you're getting "Access is denied" errors:
echo.
echo 1. EXTRACT FILES TO A USER DIRECTORY:
echo    • Desktop: C:\Users\%USERNAME%\Desktop\ExcelReportGenerator\
echo    • Documents: C:\Users\%USERNAME%\Documents\ExcelReportGenerator\
echo    • NOT in C:\Windows\System32\ or Program Files
echo.
echo 2. CLOSE ANY ANTIVIRUS REAL-TIME SCANNING temporarily
echo.
echo 3. TRY MANUAL INSTALLATION:
echo    • Open Command Prompt in the extracted folder
echo    • Run: python -m venv venv
echo    • Run: venv\Scripts\activate
echo    • Run: pip install -r requirements.txt
echo    • Run: python main.py
echo.
echo 4. CHECK PYTHON INSTALLATION:
echo    • Reinstall Python with "Add to PATH" checked
echo    • Use Python 3.7-3.11 (avoid very latest versions)
echo.

echo Press any key to exit...
pause >nul 