import os
import sys
import shutil
from pathlib import Path

def build_executable():
    """Build the standalone executable using PyInstaller"""
    print("Building standalone executable...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Clean up previous builds
    dist_dir = current_dir / "dist"
    build_dir = current_dir / "build"
    spec_file = current_dir / "main.spec"
    
    for path in [dist_dir, build_dir, spec_file]:
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)
    
    # Verify required directories exist
    required_dirs = ['templates', 'gui', 'core', 'utils']
    for dir_name in required_dirs:
        if not (current_dir / dir_name).exists():
            print(f"Error: Required directory '{dir_name}' not found!")
            sys.exit(1)
    
    # Build command
    build_cmd = [
        "pyinstaller",
        "--name=ExcelReportGenerator",
        "--onefile",
        "--windowed",
        "--add-data=templates;templates",
        "--add-data=gui;gui",
        "--add-data=core;core",
        "--add-data=utils;utils",
        "--hidden-import=customtkinter",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=jinja2",
        "--hidden-import=matplotlib",
        "--hidden-import=seaborn",
        "main.py"
    ]
    
    # Execute PyInstaller
    result = os.system(" ".join(build_cmd))
    
    if result != 0:
        print("\nError: Build failed!")
        sys.exit(1)
    
    # Verify the executable was created
    exe_path = dist_dir / "ExcelReportGenerator.exe"
    if not exe_path.exists():
        print("\nError: Executable was not created!")
        sys.exit(1)
    
    print("\nBuild completed successfully!")
    print(f"Executable can be found in: {exe_path}")
    print("\nNote: The executable is large because it includes Python and all dependencies.")
    print("First run might take a few seconds as it extracts its components.")

if __name__ == "__main__":
    build_executable() 