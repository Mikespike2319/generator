import os
import json
from typing import Dict, Any
import logging
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        # Use AppData for Windows
        self._config_dir = Path(os.getenv('APPDATA')) / 'HospitalReportGenerator'
        self._config_file = self._config_dir / 'config.json'
        self._config: Dict[str, Any] = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default if not exists."""
        if not self._config_dir.exists():
            self._config_dir.mkdir(parents=True)
            
        if not self._config_file.exists():
            default_config = {
                'theme': 'dark',
                'last_directory': str(Path.home()),
                'recent_files': [],
                'window_size': {
                    'width': 1200,
                    'height': 800
                },
                'report_settings': {
                    'default_output_dir': str(Path.home() / 'Documents' / 'Hospital Reports'),
                    'auto_open_reports': True
                }
            }
            self._save_config(default_config)
            return default_config
            
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self._logger.error(f"Failed to load config: {str(e)}")
            return {}
            
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            self._logger.error(f"Failed to save config: {str(e)}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
        self._save_config(self._config)
        
    def add_recent_file(self, file_path: str) -> None:
        """Add a file to recent files list."""
        recent_files = self.get('recent_files', [])
        if file_path in recent_files:
            recent_files.remove(file_path)
        recent_files.insert(0, file_path)
        recent_files = recent_files[:10]  # Keep only last 10 files
        self.set('recent_files', recent_files)
        
    def get_recent_files(self) -> list:
        """Get list of recent files."""
        return self.get('recent_files', [])
        
    def get_last_directory(self) -> str:
        """Get last used directory."""
        return self.get('last_directory', str(Path.home()))
        
    def set_last_directory(self, directory: str) -> None:
        """Set last used directory."""
        self.set('last_directory', directory)
        
    def get_window_size(self) -> Dict[str, int]:
        """Get window size."""
        return self.get('window_size', {'width': 1200, 'height': 800})
        
    def set_window_size(self, width: int, height: int) -> None:
        """Set window size."""
        self.set('window_size', {'width': width, 'height': height})
        
    def get_report_settings(self) -> Dict[str, Any]:
        """Get report settings."""
        return self.get('report_settings', {
            'default_output_dir': str(Path.home() / 'Documents' / 'Hospital Reports'),
            'auto_open_reports': True
        })
        
    def set_report_settings(self, settings: Dict[str, Any]) -> None:
        """Set report settings."""
        self.set('report_settings', settings) 