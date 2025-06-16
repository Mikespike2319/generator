import os
import sys
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent

def ensure_directory(path):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)
    
def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def safe_filename(filename):
    """Create a safe filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename 