import pytest
from unittest.mock import Mock, patch
import customtkinter as ctk
from hospital_report_generator.ui.main_window import MainWindow

@pytest.fixture
def mock_data_processor():
    """Create a mock data processor."""
    processor = Mock()
    processor.has_data.return_value = False
    return processor

@pytest.fixture
def mock_report_generator():
    """Create a mock report generator."""
    generator = Mock()
    generator.generate_report.return_value = "<html>Test Report</html>"
    return generator

@pytest.fixture
def mock_config_manager():
    """Create a mock configuration manager."""
    config = Mock()
    config.get.return_value = {
        'width': 1200,
        'height': 800
    }
    return config

@pytest.fixture
def main_window(mock_data_processor, mock_report_generator, mock_config_manager):
    """Create a MainWindow instance with mocked dependencies."""
    with patch('hospital_report_generator.ui.main_window.DataProcessor', return_value=mock_data_processor), \
         patch('hospital_report_generator.ui.main_window.ReportGenerator', return_value=mock_report_generator), \
         patch('hospital_report_generator.ui.main_window.ConfigManager', return_value=mock_config_manager):
        window = MainWindow()
        return window

def test_window_initialization(main_window):
    """Test window initialization."""
    assert isinstance(main_window, ctk.CTk)
    assert main_window.title() == "Hospital Report Generator"
    
    # Check if main widgets are created
    assert hasattr(main_window, 'main_frame')
    assert hasattr(main_window, 'header')
    assert hasattr(main_window, 'content_frame')
    assert hasattr(main_window, 'file_frame')
    assert hasattr(main_window, 'options_frame')
    assert hasattr(main_window, 'generate_btn')

def test_select_file(main_window, mock_data_processor):
    """Test file selection."""
    with patch('tkinter.filedialog.askopenfilename', return_value='test.xlsx'):
        main_window.select_file()
        mock_data_processor.load_data.assert_called_once_with('test.xlsx')

def test_generate_report_no_file(main_window, mock_data_processor):
    """Test report generation without file."""
    mock_data_processor.has_data.return_value = False
    main_window.generate_report()
    # Should show error message

def test_generate_report_with_file(main_window, mock_data_processor, mock_report_generator):
    """Test report generation with file."""
    mock_data_processor.has_data.return_value = True
    mock_data_processor.get_data.return_value = "test_data"
    
    with patch('webbrowser.open') as mock_browser:
        main_window.generate_report()
        mock_report_generator.generate_report.assert_called_once()
        mock_browser.assert_called_once()

def test_report_type_selection(main_window):
    """Test report type selection."""
    # Check default value
    assert main_window.report_type.get() == 'summary'
    
    # Change selection
    main_window.report_type.set('demographics')
    assert main_window.report_type.get() == 'demographics'

def test_theme_settings(main_window):
    """Test theme settings."""
    assert ctk.get_appearance_mode() == "dark"
    assert ctk.get_default_color_theme() == "blue" 