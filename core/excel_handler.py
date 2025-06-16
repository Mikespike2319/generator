import pandas as pd
import os
from pathlib import Path

class ExcelHandler:
    """Handles Excel file loading and basic processing"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
        
    def load_file(self, file_path):
        """
        Load Excel file and return pandas DataFrame
        
        Args:
            file_path (str): Path to Excel file
            
        Returns:
            pandas.DataFrame: Loaded data
        """
        if not self.is_valid_file(file_path):
            raise ValueError(f"Unsupported file format. Supported formats: {self.supported_formats}")
            
        try:
            # Try to load the file
            if file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path, engine='openpyxl')
            else:
                data = pd.read_excel(file_path, engine='xlrd')
                
            # Basic data cleaning
            data = self.clean_data(data)
            
            return data
            
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
            
    def is_valid_file(self, file_path):
        """Check if file is a valid Excel file"""
        if not os.path.exists(file_path):
            return False
            
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.supported_formats
        
    def clean_data(self, data):
        """
        Perform basic data cleaning
        
        Args:
            data (pandas.DataFrame): Raw data
            
        Returns:
            pandas.DataFrame: Cleaned data
        """
        # Remove completely empty rows and columns
        data = data.dropna(how='all')
        data = data.dropna(axis=1, how='all')
        
        # Reset index
        data = data.reset_index(drop=True)
        
        # Clean column names
        data.columns = [str(col).strip() for col in data.columns]
        
        return data
        
    def get_sheet_names(self, file_path):
        """
        Get all sheet names from Excel file
        
        Args:
            file_path (str): Path to Excel file
            
        Returns:
            list: List of sheet names
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            raise Exception(f"Error reading sheet names: {str(e)}")
            
    def load_specific_sheet(self, file_path, sheet_name):
        """
        Load specific sheet from Excel file
        
        Args:
            file_path (str): Path to Excel file
            sheet_name (str): Name of sheet to load
            
        Returns:
            pandas.DataFrame: Loaded data from specific sheet
        """
        try:
            data = pd.read_excel(file_path, sheet_name=sheet_name)
            return self.clean_data(data)
        except Exception as e:
            raise Exception(f"Error loading sheet '{sheet_name}': {str(e)}")
            
    def get_file_info(self, file_path):
        """
        Get basic information about Excel file
        
        Args:
            file_path (str): Path to Excel file
            
        Returns:
            dict: File information
        """
        try:
            data = self.load_file(file_path)
            
            info = {
                'filename': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'rows': len(data),
                'columns': len(data.columns),
                'column_names': list(data.columns),
                'data_types': data.dtypes.to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum()
            }
            
            return info
            
        except Exception as e:
            raise Exception(f"Error getting file info: {str(e)}") 