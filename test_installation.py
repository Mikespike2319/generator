import sys
import importlib.util
import os

def check_package(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} is not installed")
        return False
    print(f"✅ {package_name} is installed")
    return True

def main():
    print("Testing Hospital Report Generator Installation...")
    print("=" * 50)
    
    # Test Python version
    print(f"✓ Python version: {sys.version}")
    
    # Test required modules
    try:
        import pandas as pd
        print("✓ pandas installed successfully")
    except ImportError:
        print("✗ pandas not found - run: pip install pandas")

    try:
        import openpyxl
        print("✓ openpyxl installed successfully")
    except ImportError:
        print("✗ openpyxl not found - run: pip install openpyxl")

    try:
        import PyInstaller
        print("✓ PyInstaller installed successfully")
    except ImportError:
        print("✗ PyInstaller not found - run: pip install pyinstaller")

    # Test tkinter (should be included with Python)
    try:
        import tkinter
        print("✓ tkinter available (GUI framework)")
    except ImportError:
        print("✗ tkinter not available - may need to reinstall Python")

    print("=" * 50)
    print("Installation test complete!")
    print("If all items show ✓, you're ready to run the application!")

    input("Press Enter to close...")

if __name__ == "__main__":
    main() 