# Excel Data Analysis Report Generator (Windows)

A professional Windows application for converting Excel files into beautiful HTML reports with data analysis and visualizations.

## 🖥️ Windows Installation

### Quick Start (Recommended)
1. **Download** the repository as a ZIP file from GitHub
2. **Extract** to your desired location (e.g., `C:\ExcelReportGenerator\`)
3. **Double-click** `run.bat` to automatically install and run

The batch file will:
- ✅ Check if Python is installed
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Launch the application

### Manual Installation
If you prefer manual setup:

```batch
# Open Command Prompt in the project folder
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📋 Requirements

- **Windows 10/11** (Primary support)
- **Python 3.7+** ([Download from python.org](https://python.org))
  - ⚠️ **Important**: Check "Add Python to PATH" during installation
- **Excel files** (.xlsx or .xls format)

## 🚀 How to Use

1. **Launch**: Double-click `run.bat` or run `python main.py`
2. **Select Excel File**: Click "Browse Files" and choose your data file
3. **Preview Data**: See real-time preview with basic statistics
4. **Choose Report Type**:
   - **Summary Report**: Quick overview with key metrics
   - **Detailed Analysis**: Column-by-column breakdown
   - **Data Overview**: Basic structure and data types
5. **Generate Report**: Click "Generate Report" for professional HTML output
6. **View Results**: Report automatically opens in your default browser

## 📊 Generated Reports Include

### Professional Layout
- **Landscape Format**: Optimized for printing and viewing
- **Two-Column Grid**: Organized sections with clear hierarchy
- **Status Indicators**: Green (●) for good, Red (⚠) for issues
- **Color-Coded Tables**: Visual status representation

### Data Analysis
- **Data Overview**: Record counts, field analysis, completeness metrics
- **Column Analysis**: Data types, null counts, unique values
- **Visual Charts**: Completeness graphs, data type distribution
- **Statistical Analysis**: Mean, median, min/max for numeric data
- **Quality Assessment**: Missing values, duplicates, recommendations

### Professional Features
- **Print-Ready**: Letter landscape format with proper margins
- **Action Items**: Specific recommendations based on analysis
- **Alert Boxes**: Highlighted warnings for critical issues
- **Compliance Status**: Clear indicators for data quality

## 📁 Project Structure

```
ExcelReportGenerator/
├── run.bat                 # Windows launcher (double-click to run)
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── gui/
│   └── main_window.py      # Windows GUI interface
├── core/
│   ├── excel_handler.py    # Excel file processing
│   ├── data_processor.py   # Data analysis engine
│   └── report_generator.py # HTML report creation
├── templates/
│   └── report_template.html # Professional report template
├── utils/
│   └── helpers.py          # Utility functions
├── venv/                   # Virtual environment (auto-created)
└── reports/                # Generated reports (auto-created)
```

## 🔧 Dependencies (Auto-installed)

- **customtkinter** - Modern Windows GUI
- **pandas** - Excel data processing
- **openpyxl** - Excel file support (.xlsx)
- **jinja2** - HTML template engine
- **matplotlib** - Chart generation
- **seaborn** - Enhanced visualizations

## 🛠️ Troubleshooting

### Common Issues

**"Python is not recognized"**
- Install Python from [python.org](https://python.org)
- ✅ Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

**"Failed to install dependencies"**
- Ensure internet connection is active
- Try running as Administrator
- Update pip: `python -m pip install --upgrade pip`

**"Excel file won't load"**
- Verify file format is .xlsx or .xls
- Check file isn't password protected
- Ensure file isn't open in Excel

**GUI doesn't appear**
- Check Windows Defender/Antivirus settings
- Ensure tkinter is installed (comes with Python)
- Try running from Command Prompt to see error messages

### Performance Tips
- Close Excel before processing large files
- For files >100MB, use "Data Overview" report type
- Generated reports are saved in `reports/` folder

## 📄 Report Output

Reports are saved as HTML files in the `reports/` folder with timestamps:
- `report_summary_20241201_143022.html`
- Automatically opens in default browser
- Print-ready landscape format
- Professional styling for presentations

## 🔒 Privacy & Security

- **100% Local Processing** - No data sent to external servers
- **Offline Operation** - Works without internet connection
- **Secure** - All processing happens on your Windows machine
- **No Data Storage** - Original files remain unchanged

## 📞 Support

For Windows-specific issues:
1. Check Python installation and PATH
2. Run `run.bat` from Command Prompt to see detailed error messages
3. Ensure all dependencies installed correctly
4. Verify Excel file format and accessibility

## 📝 License

MIT License - Free for personal and commercial use on Windows systems. 