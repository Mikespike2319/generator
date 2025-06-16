# Hospital Report Generator

A professional desktop application for generating hospital reports in HTML format, designed to match Tallahassee Memorial Hospital standards. The application features a modern, user-friendly interface and powerful reporting capabilities.

## Features

- Modern, dark-themed UI with customtkinter
- 5 different report types:
  - Daily Patient Summary
  - Department Statistics
  - Resource Utilization
  - Quality Metrics
  - Financial Overview
- Professional HTML output with hospital-standard styling
- Interactive charts and visualizations using Chart.js
- Excel data import support
- Recent files history
- Configurable settings
- Comprehensive logging
- Automated report generation with timestamps

## Installation (Windows)

### Option 1: Using the Executable (Recommended)

1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `HospitalReportGenerator.exe`

### Option 2: From Source

1. Ensure you have Python 3.8 or higher installed
2. Clone this repository
3. Run the setup script:
   ```batch
   run.bat
   ```
   This will:
   - Create a virtual environment
   - Install required dependencies
   - Launch the application

## Usage

1. Launch the application using one of the methods above
2. Select the report type
3. Choose your Excel data file
4. Click "Generate Report"

## Project Structure

```
hospital_report_generator/
├── src/
│   ├── core/
│   │   ├── data_processor.py
│   │   └── report_generator.py
│   ├── ui/
│   │   └── main_window.py
│   ├── utils/
│   │   └── config_manager.py
│   └── main.py
├── tests/
│   ├── test_data_processor.py
│   ├── test_report_generator.py
│   ├── test_main_window.py
│   └── test_config_manager.py
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── run.bat
├── build.bat
└── README.md
```

## Configuration

The application stores its configuration in `%APPDATA%\HospitalReportGenerator\config.json`. You can modify:
- Theme settings
- Window size
- Recent files
- Report output directory
- Auto-open reports setting

## Logging

Logs are stored in `%APPDATA%\HospitalReportGenerator\logs\app.log`. The application logs:
- Application startup and shutdown
- File operations
- Report generation
- Errors and exceptions

## Building Executable

To create a standalone Windows executable:

1. Run the build script:
   ```batch
   build.bat
   ```
2. The executable will be created in the `dist` folder

## Development

1. Install development dependencies:
   ```batch
   pip install -r requirements-dev.txt
   ```
2. Run tests:
   ```batch
   pytest
   ```
3. Format code:
   ```batch
   black src/
   ```
4. Lint code:
   ```batch
   flake8 src/
   ```

## Troubleshooting

If you encounter any issues:

1. Check the log file at `%APPDATA%\HospitalReportGenerator\logs\app.log`
2. Ensure you have the latest version of Python installed
3. Try running the application from source using `run.bat`
4. Check that all required Excel files are properly formatted

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository. 