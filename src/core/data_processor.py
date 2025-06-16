import pandas as pd
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._logger = logging.getLogger(__name__)
        
    def load_data(self, file_path: str, sheet_name: str = "Sheet1") -> None:
        """
        Load data from an Excel file.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str): Name of the sheet to load
            
        Raises:
            ValueError: If the file cannot be loaded or is invalid
        """
        try:
            # Read Excel file
            self._data = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Convert date columns to datetime
            self._convert_date_columns()
            
            # Validate data
            self._validate_data()
            
            self._logger.info(f"Successfully loaded data from {file_path}")
        except Exception as e:
            self._logger.error(f"Failed to load data from {file_path}: {str(e)}")
            raise ValueError(f"Failed to load Excel file: {str(e)}")
    
    def _convert_date_columns(self) -> None:
        """Convert date columns to datetime format."""
        if self._data is None:
            return
            
        # Common date column names
        date_columns = ['Date', 'AdmissionDate', 'DischargeDate', 'VisitDate']
        
        for col in date_columns:
            if col in self._data.columns:
                try:
                    self._data[col] = pd.to_datetime(self._data[col])
                except Exception as e:
                    self._logger.warning(f"Could not convert {col} to datetime: {str(e)}")
    
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
            
        # Check for data types
        if not pd.api.types.is_numeric_dtype(self._data['PatientID']):
            self._data['PatientID'] = self._data['PatientID'].astype(str)
    
    def get_data(self, date_range: Optional[str] = None) -> pd.DataFrame:
        """
        Get the loaded data, optionally filtered by date range.
        
        Args:
            date_range (str, optional): Date range to filter by
                ("Last Month", "Last 3 Months", "Last 6 Months", "Last Year")
                
        Returns:
            pd.DataFrame: The filtered data
            
        Raises:
            ValueError: If no data is loaded
        """
        if self._data is None:
            raise ValueError("No data loaded")
            
        if date_range and 'Date' in self._data.columns:
            today = datetime.now()
            
            if date_range == "Last Month":
                start_date = today - timedelta(days=30)
            elif date_range == "Last 3 Months":
                start_date = today - timedelta(days=90)
            elif date_range == "Last 6 Months":
                start_date = today - timedelta(days=180)
            elif date_range == "Last Year":
                start_date = today - timedelta(days=365)
            else:
                return self._data
                
            return self._data[self._data['Date'] >= start_date]
            
        return self._data
    
    def has_data(self) -> bool:
        """Check if data is loaded."""
        return self._data is not None and not self._data.empty
    
    def get_column_names(self) -> List[str]:
        """Get list of column names."""
        if self._data is None:
            return []
        return list(self._data.columns)
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the data."""
        if self._data is None:
            return {}
            
        summary = {
            'total_rows': len(self._data),
            'columns': list(self._data.columns),
            'date_range': {
                'start': self._data['Date'].min().strftime('%Y-%m-%d'),
                'end': self._data['Date'].max().strftime('%Y-%m-%d')
            } if 'Date' in self._data.columns else None,
            'departments': self._data['Department'].unique().tolist() if 'Department' in self._data.columns else []
        }
        
        return summary
    
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