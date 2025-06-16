import pytest
import pandas as pd
from pathlib import Path
from hospital_report_generator.core.data_processor import DataProcessor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'PatientID': ['P001', 'P002', 'P003'],
        'Date': pd.date_range(start='2024-01-01', periods=3),
        'Department': ['Cardiology', 'Neurology', 'Cardiology'],
        'Age': [45, 60, 55],
        'Gender': ['M', 'F', 'M'],
        'AdmissionType': ['Emergency', 'Planned', 'Emergency'],
        'LengthOfStay': [3, 5, 2]
    })

@pytest.fixture
def data_processor():
    """Create a DataProcessor instance for testing."""
    return DataProcessor()

def test_load_data(data_processor, sample_data, tmp_path):
    """Test loading data from Excel file."""
    # Create temporary Excel file
    excel_file = tmp_path / "test_data.xlsx"
    sample_data.to_excel(excel_file, index=False)
    
    # Test loading data
    data_processor.load_data(str(excel_file))
    assert data_processor.has_data()
    assert len(data_processor.get_data()) == 3

def test_validate_data(data_processor, sample_data):
    """Test data validation."""
    data_processor._data = sample_data
    data_processor._validate_data()  # Should not raise any exception
    
    # Test with missing required column
    invalid_data = sample_data.drop(columns=['PatientID'])
    data_processor._data = invalid_data
    with pytest.raises(ValueError):
        data_processor._validate_data()

def test_get_summary_stats(data_processor, sample_data):
    """Test getting summary statistics."""
    data_processor._data = sample_data
    stats = data_processor.get_summary_stats()
    
    assert stats['total_patients'] == 3
    assert stats['total_records'] == 3
    assert len(stats['departments']) == 2
    assert 'Cardiology' in stats['departments']
    assert 'Neurology' in stats['departments']

def test_get_department_stats(data_processor, sample_data):
    """Test getting department statistics."""
    data_processor._data = sample_data
    dept_stats = data_processor.get_department_stats()
    
    assert len(dept_stats) == 2
    assert 'Cardiology' in dept_stats['Department'].values
    assert 'Neurology' in dept_stats['Department'].values 