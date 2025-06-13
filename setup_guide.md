# Hospital Report Generator - Setup Guide

## Prerequisites

- Windows 10 or later
- Python 3.8 or higher
- Internet connection for downloading dependencies

## Installation Steps

### 1. Python Installation

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### 2. Project Setup

1. Download or clone the repository
2. Open Command Prompt in the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Testing the Installation

1. Run the test script:
   ```bash
   python test_installation.py
   ```
2. Verify all checks pass

### 4. Building the Executable

1. Run the build script:
   ```bash
   build.bat
   ```
2. Wait for the build process to complete
3. Find the executable in the `dist` folder

## Usage Guide

### Running the Application

1. Double-click the executable in the `dist` folder
2. Or run from command line:
   ```bash
   python hospital_report_generator.py
   ```

### Generating Reports

1. Select report type from the dropdown
2. Enter report date (defaults to current date)
3. Click "Browse" to select Excel data file
4. Click "Generate Report"
5. Report will open in default web browser

### Excel File Format

Your Excel file should contain the following columns:
- For Patient Summary: patient_id, admission_date, discharge_date, length_of_stay
- For Department Stats: department, patients, utilization
- For other reports: relevant metrics as needed

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`

2. **Excel File Not Found**
   - Ensure file path is correct
   - Check file permissions

3. **Report Generation Fails**
   - Verify Excel file format
   - Check data column names

### Getting Help

If you encounter issues:
1. Check the error message
2. Verify all prerequisites are met
3. Open an issue on GitHub

## Maintenance

### Updating Dependencies

1. Activate virtual environment
2. Run: `pip install --upgrade -r requirements.txt`

### Backup

1. Regularly backup your Excel data files
2. Keep copies of generated reports

## Security Notes

- Keep your Python installation updated
- Don't share sensitive hospital data
- Use secure file locations for data storage 