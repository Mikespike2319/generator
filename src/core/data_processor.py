import pandas as pd
from typing import Optional, Dict, Any
import logging

class DataProcessor:
    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._logger = logging.getLogger(__name__)
        
    def load_data(self, file_path: str) -> None:
        """
        Load data from an Excel file.
        
        Args:
            file_path (str): Path to the Excel file
            
        Raises:
            ValueError: If the file cannot be loaded or is invalid
        """
        try:
            self._data = pd.read_excel(file_path)
            self._validate_data()
            self._logger.info(f"Successfully loaded data from {file_path}")
        except Exception as e:
            self._logger.error(f"Failed to load data from {file_path}: {str(e)}")
            raise ValueError(f"Failed to load Excel file: {str(e)}")
    
    def _validate_data(self) -> None:
        """
        Validate the loaded data.
        
        Raises:
            ValueError: If the data is invalid
        """
        if self._data is None:
            raise ValueError("No data loaded")
            
        if self._data.empty:
            raise ValueError("Excel file contains no data")
            
        # Check for required columns
        required_columns = ['PatientID', 'Date', 'Department']
        missing_columns = [col for col in required_columns if col not in self._data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the loaded data.
        
        Returns:
            pd.DataFrame: The loaded data
            
        Raises:
            ValueError: If no data is loaded
        """
        if self._data is None:
            raise ValueError("No data loaded")
        return self._data
    
    def has_data(self) -> bool:
        """
        Check if data is loaded.
        
        Returns:
            bool: True if data is loaded, False otherwise
        """
        return self._data is not None
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics for the loaded data.
        
        Returns:
            Dict[str, Any]: Dictionary containing summary statistics
            
        Raises:
            ValueError: If no data is loaded
        """
        if not self.has_data():
            raise ValueError("No data loaded")
            
        return {
            'total_patients': len(self._data['PatientID'].unique()),
            'total_records': len(self._data),
            'date_range': {
                'start': self._data['Date'].min(),
                'end': self._data['Date'].max()
            },
            'departments': self._data['Department'].unique().tolist()
        }
    
    def get_department_stats(self) -> pd.DataFrame:
        """
        Get statistics by department.
        
        Returns:
            pd.DataFrame: Department statistics
            
        Raises:
            ValueError: If no data is loaded
        """
        if not self.has_data():
            raise ValueError("No data loaded")
            
        return self._data.groupby('Department').agg({
            'PatientID': 'count',
            'Date': ['min', 'max']
        }).reset_index() 