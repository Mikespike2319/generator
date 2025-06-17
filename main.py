"""
Excel Data Analysis Report Generator (Windows)
A professional Windows application for converting Excel files to HTML reports
"""

import sys
import os
from pathlib import Path

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent

    return os.path.join(base_path, relative_path)

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    import customtkinter as ctk
    from gui.main_window import MainWindow
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point for the application"""
    # Set appearance mode and theme
    ctk.set_appearance_mode("system")  # "system", "dark", "light"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
    
    # Create and run the application
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 