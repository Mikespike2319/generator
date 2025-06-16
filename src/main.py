import sys
import logging
from pathlib import Path
import os
import customtkinter as ctk
from ui.main_window import MainWindow

def setup_logging():
    """Set up logging configuration."""
    # Use AppData for Windows
    log_dir = Path(os.getenv('APPDATA')) / 'HospitalReportGenerator' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the application."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Set working directory to the executable's directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            os.chdir(os.path.dirname(sys.executable))
        else:
            # Running as script
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Initialize customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create and run the main window
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 