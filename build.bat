@echo off
echo Building Hospital Report Generator...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
pip install -r requirements-dev.txt

REM Create executable
echo Creating executable...
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "src;src" ^
    --icon "src/assets/icon.ico" ^
    --name "HospitalReportGenerator" ^
    src/main.py

REM Create output directory
if not exist "dist\HospitalReportGenerator" mkdir "dist\HospitalReportGenerator"

REM Copy additional files
echo Copying additional files...
copy "README.md" "dist\HospitalReportGenerator\"
copy "LICENSE" "dist\HospitalReportGenerator\"

echo Build complete! The executable is in the dist folder.
pause 