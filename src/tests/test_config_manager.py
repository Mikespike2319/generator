import pytest
from pathlib import Path
import json
import shutil
from hospital_report_generator.utils.config_manager import ConfigManager

@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / '.hospital_report_generator'
    config_dir.mkdir()
    return config_dir

@pytest.fixture
def config_manager(temp_config_dir, monkeypatch):
    """Create a ConfigManager instance with temporary config directory."""
    monkeypatch.setattr(Path, 'home', lambda: temp_config_dir.parent)
    return ConfigManager()

def test_default_config(config_manager):
    """Test default configuration values."""
    assert config_manager.get('theme') == 'dark'
    assert config_manager.get('last_directory') == str(Path.home())
    assert config_manager.get('recent_files') == []
    assert config_manager.get('window_size') == {'width': 1200, 'height': 800}

def test_set_and_get_config(config_manager):
    """Test setting and getting configuration values."""
    config_manager.set('test_key', 'test_value')
    assert config_manager.get('test_key') == 'test_value'
    
    config_manager.set('test_dict', {'key': 'value'})
    assert config_manager.get('test_dict') == {'key': 'value'}

def test_recent_files(config_manager):
    """Test recent files functionality."""
    # Add files
    config_manager.add_recent_file('file1.xlsx')
    config_manager.add_recent_file('file2.xlsx')
    
    # Check recent files
    recent_files = config_manager.get_recent_files()
    assert len(recent_files) == 2
    assert recent_files[0] == 'file2.xlsx'
    assert recent_files[1] == 'file1.xlsx'
    
    # Test maximum number of recent files
    for i in range(10):
        config_manager.add_recent_file(f'file{i}.xlsx')
    
    recent_files = config_manager.get_recent_files()
    assert len(recent_files) == 10

def test_window_size(config_manager):
    """Test window size configuration."""
    config_manager.set_window_size(800, 600)
    window_size = config_manager.get_window_size()
    assert window_size['width'] == 800
    assert window_size['height'] == 600

def test_report_settings(config_manager):
    """Test report settings configuration."""
    settings = {
        'default_output_dir': '/custom/path',
        'auto_open_reports': False
    }
    config_manager.set_report_settings(settings)
    
    saved_settings = config_manager.get_report_settings()
    assert saved_settings['default_output_dir'] == '/custom/path'
    assert saved_settings['auto_open_reports'] is False

def test_config_persistence(config_manager, temp_config_dir):
    """Test that configuration persists between instances."""
    # Set some values
    config_manager.set('test_key', 'test_value')
    config_manager.add_recent_file('test.xlsx')
    
    # Create new instance
    new_config_manager = ConfigManager()
    
    # Check values
    assert new_config_manager.get('test_key') == 'test_value'
    assert 'test.xlsx' in new_config_manager.get_recent_files() 