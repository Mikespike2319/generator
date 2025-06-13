@echo off
echo ================================================
echo Hospital Report Generator - Build Script
echo ================================================
echo.

echo Installing required packages...
pip install pandas openpyxl pyinstaller
echo.

echo Building executable...
pyinstaller --onefile --windowed --name "HospitalReportGenerator" hospital_report_generator.py
echo.

echo Cleaning up build files...
rmdir /s /q build
del HospitalReportGenerator.spec
echo.

echo ================================================
echo Build Complete!
echo ================================================
echo Your executable is located at: dist\HospitalReportGenerator.exe
echo.
pause 