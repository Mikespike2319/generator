# Hospital Report Generator

A modern Python application for generating hospital reports with a beautiful UI.

## Installation (Windows)

1. Download the repository as a ZIP file from GitHub
2. Extract the ZIP file to a location of your choice
3. Double-click `run.bat` to start the application

The `run.bat` script will automatically:
- Check if Python is installed
- Create a virtual environment if needed
- Install all required dependencies
- Start the application

### Manual Installation (Alternative Method)

If you prefer to install manually, open Command Prompt and run:

```batch
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Run the application
python -m hospital_report_generator
```

## Running Tests

To run the test suite:

```batch
# Make sure you're in the virtual environment
pytest
```

## Features

- Modern, user-friendly interface
- Support for multiple report types
- Excel file processing
- HTML report generation
- Configurable settings

## Requirements

- Windows operating system
- Python 3.8 or higher

## Dependencies

The following packages will be automatically installed:
- customtkinter
- pandas
- openpyxl
- pytest (for development)

## Troubleshooting

If you encounter any issues:

1. Make sure you have Python 3.8 or higher installed
2. Ensure you're running the commands from the correct directory
3. Verify that the virtual environment is activated
4. Check that all dependencies are installed correctly

## Support

For issues or questions, please open an issue on the GitHub repository. 