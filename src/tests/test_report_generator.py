import pytest
import pandas as pd
from hospital_report_generator.core.report_generator import ReportGenerator

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
def report_generator():
    """Create a ReportGenerator instance for testing."""
    return ReportGenerator()

def test_generate_summary_report(report_generator, sample_data):
    """Test generating summary report."""
    html_content = report_generator.generate_report(sample_data, 'summary')
    
    # Check for key elements in the HTML
    assert '<!DOCTYPE html>' in html_content
    assert 'Hospital Summary Report' in html_content
    assert 'Total Patients' in html_content
    assert 'Total Records' in html_content
    assert 'Cardiology' in html_content
    assert 'Neurology' in html_content

def test_generate_demographics_report(report_generator, sample_data):
    """Test generating demographics report."""
    html_content = report_generator.generate_report(sample_data, 'demographics')
    
    # Check for key elements in the HTML
    assert '<!DOCTYPE html>' in html_content
    assert 'Hospital Demographics Report' in html_content
    assert 'Age Distribution' in html_content
    assert 'Gender Distribution' in html_content
    assert 'Admission Types' in html_content
    assert 'Chart.js' in html_content

def test_generate_department_report(report_generator, sample_data):
    """Test generating department report."""
    html_content = report_generator.generate_report(sample_data, 'department')
    
    # Check for key elements in the HTML
    assert '<!DOCTYPE html>' in html_content
    assert 'Hospital Department Report' in html_content
    assert 'Department Statistics' in html_content
    assert 'Cardiology' in html_content
    assert 'Neurology' in html_content

def test_generate_monthly_report(report_generator, sample_data):
    """Test generating monthly report."""
    html_content = report_generator.generate_report(sample_data, 'monthly')
    
    # Check for key elements in the HTML
    assert '<!DOCTYPE html>' in html_content
    assert 'Hospital Monthly Report' in html_content
    assert 'Monthly Statistics' in html_content
    assert '2024-01' in html_content

def test_generate_custom_report(report_generator, sample_data):
    """Test generating custom report."""
    html_content = report_generator.generate_report(sample_data, 'custom')
    
    # Check for key elements in the HTML
    assert '<!DOCTYPE html>' in html_content
    assert 'Hospital Custom Report' in html_content
    assert 'P001' in html_content
    assert 'P002' in html_content
    assert 'P003' in html_content

def test_invalid_report_type(report_generator, sample_data):
    """Test handling invalid report type."""
    with pytest.raises(ValueError):
        report_generator.generate_report(sample_data, 'invalid_type')

def test_report_templates_loaded(report_generator):
    """Test that all report templates are loaded."""
    assert 'summary' in report_generator._templates
    assert 'demographics' in report_generator._templates
    assert 'department' in report_generator._templates
    assert 'monthly' in report_generator._templates
    assert 'custom' in report_generator._templates 