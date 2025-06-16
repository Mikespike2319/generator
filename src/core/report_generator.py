import pandas as pd
from typing import Dict, Any
from datetime import datetime
import logging
from jinja2 import Template

class ReportGenerator:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Template]:
        """Load HTML templates for different report types."""
        return {
            'summary': Template(self._get_summary_template()),
            'demographics': Template(self._get_demographics_template()),
            'department': Template(self._get_department_template()),
            'monthly': Template(self._get_monthly_template()),
            'custom': Template(self._get_custom_template())
        }
    
    def generate_report(self, data: pd.DataFrame, report_type: str) -> str:
        """
        Generate an HTML report based on the data and report type.
        
        Args:
            data (pd.DataFrame): The data to generate the report from
            report_type (str): The type of report to generate
            
        Returns:
            str: The generated HTML report
            
        Raises:
            ValueError: If the report type is invalid
        """
        if report_type not in self._templates:
            raise ValueError(f"Invalid report type: {report_type}")
            
        try:
            template = self._templates[report_type]
            context = self._prepare_context(data, report_type)
            return template.render(**context)
        except Exception as e:
            self._logger.error(f"Failed to generate {report_type} report: {str(e)}")
            raise
    
    def _prepare_context(self, data: pd.DataFrame, report_type: str) -> Dict[str, Any]:
        """Prepare the context data for the template."""
        context = {
            'title': f"Hospital {report_type.title()} Report",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hospital_name': "Tallahassee Memorial Hospital"
        }
        
        if report_type == 'summary':
            context.update(self._prepare_summary_context(data))
        elif report_type == 'demographics':
            context.update(self._prepare_demographics_context(data))
        elif report_type == 'department':
            context.update(self._prepare_department_context(data))
        elif report_type == 'monthly':
            context.update(self._prepare_monthly_context(data))
        elif report_type == 'custom':
            context.update(self._prepare_custom_context(data))
            
        return context
    
    def _prepare_summary_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for summary report."""
        return {
            'total_patients': len(data['PatientID'].unique()),
            'total_records': len(data),
            'date_range': {
                'start': data['Date'].min().strftime('%Y-%m-%d'),
                'end': data['Date'].max().strftime('%Y-%m-%d')
            },
            'departments': data['Department'].unique().tolist()
        }
    
    def _prepare_demographics_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for demographics report."""
        return {
            'age_distribution': data['Age'].value_counts().to_dict(),
            'gender_distribution': data['Gender'].value_counts().to_dict(),
            'admission_types': data['AdmissionType'].value_counts().to_dict()
        }
    
    def _prepare_department_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for department report."""
        dept_stats = data.groupby('Department').agg({
            'PatientID': 'count',
            'LengthOfStay': 'mean'
        }).reset_index()
        
        return {
            'department_stats': dept_stats.to_dict('records')
        }
    
    def _prepare_monthly_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for monthly report."""
        monthly_stats = data.groupby(data['Date'].dt.to_period('M')).agg({
            'PatientID': 'count',
            'LengthOfStay': 'mean'
        }).reset_index()
        
        return {
            'monthly_stats': monthly_stats.to_dict('records')
        }
    
    def _prepare_custom_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for custom report."""
        return {
            'data': data.to_dict('records')
        }
    
    def _get_summary_template(self) -> str:
        """Get the HTML template for summary report."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #003d5c 0%, #0056b3 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .stats-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .stat-card {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .stat-card h3 {
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                }
                .stat-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #3498db;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{ hospital_name }}</h1>
                <h2>{{ title }}</h2>
                <p>Generated on: {{ generated_at }}</p>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <h3>Total Patients</h3>
                    <div class="stat-value">{{ total_patients }}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Records</h3>
                    <div class="stat-value">{{ total_records }}</div>
                </div>
                <div class="stat-card">
                    <h3>Date Range</h3>
                    <div class="stat-value">{{ date_range.start }} to {{ date_range.end }}</div>
                </div>
            </div>
            
            <div class="stat-card">
                <h3>Departments</h3>
                <ul>
                    {% for dept in departments %}
                    <li>{{ dept }}</li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
        """
    
    def _get_demographics_template(self) -> str:
        """Get the HTML template for demographics report."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                /* Same base styles as summary template */
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #003d5c 0%, #0056b3 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .chart-container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>{{ hospital_name }}</h1>
                <h2>{{ title }}</h2>
                <p>Generated on: {{ generated_at }}</p>
            </div>
            
            <div class="chart-container">
                <canvas id="ageChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="genderChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="admissionChart"></canvas>
            </div>
            
            <script>
                // Age distribution chart
                new Chart(document.getElementById('ageChart'), {
                    type: 'bar',
                    data: {
                        labels: {{ age_distribution.keys() | list | tojson }},
                        datasets: [{
                            label: 'Number of Patients',
                            data: {{ age_distribution.values() | list | tojson }},
                            backgroundColor: '#3498db'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Age Distribution'
                            }
                        }
                    }
                });
                
                // Gender distribution chart
                new Chart(document.getElementById('genderChart'), {
                    type: 'pie',
                    data: {
                        labels: {{ gender_distribution.keys() | list | tojson }},
                        datasets: [{
                            data: {{ gender_distribution.values() | list | tojson }},
                            backgroundColor: ['#3498db', '#e74c3c']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Gender Distribution'
                            }
                        }
                    }
                });
                
                // Admission types chart
                new Chart(document.getElementById('admissionChart'), {
                    type: 'bar',
                    data: {
                        labels: {{ admission_types.keys() | list | tojson }},
                        datasets: [{
                            label: 'Number of Admissions',
                            data: {{ admission_types.values() | list | tojson }},
                            backgroundColor: '#2ecc71'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Admission Types'
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
    
    def _get_department_template(self) -> str:
        """Get the HTML template for department report."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                /* Same base styles as summary template */
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #003d5c 0%, #0056b3 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .chart-container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>{{ hospital_name }}</h1>
                <h2>{{ title }}</h2>
                <p>Generated on: {{ generated_at }}</p>
            </div>
            
            <div class="chart-container">
                <canvas id="departmentChart"></canvas>
            </div>
            
            <script>
                // Department statistics chart
                new Chart(document.getElementById('departmentChart'), {
                    type: 'bar',
                    data: {
                        labels: {{ department_stats | map(attribute='Department') | list | tojson }},
                        datasets: [{
                            label: 'Number of Patients',
                            data: {{ department_stats | map(attribute='PatientID') | list | tojson }},
                            backgroundColor: '#3498db'
                        }, {
                            label: 'Average Length of Stay (days)',
                            data: {{ department_stats | map(attribute='LengthOfStay') | list | tojson }},
                            backgroundColor: '#2ecc71',
                            yAxisID: 'y1'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Department Statistics'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Number of Patients'
                                }
                            },
                            y1: {
                                beginAtZero: true,
                                position: 'right',
                                title: {
                                    display: true,
                                    text: 'Average Length of Stay (days)'
                                }
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
    
    def _get_monthly_template(self) -> str:
        """Get the HTML template for monthly report."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                /* Same base styles as summary template */
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #003d5c 0%, #0056b3 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .chart-container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>{{ hospital_name }}</h1>
                <h2>{{ title }}</h2>
                <p>Generated on: {{ generated_at }}</p>
            </div>
            
            <div class="chart-container">
                <canvas id="monthlyChart"></canvas>
            </div>
            
            <script>
                // Monthly statistics chart
                new Chart(document.getElementById('monthlyChart'), {
                    type: 'line',
                    data: {
                        labels: {{ monthly_stats | map(attribute='Date') | list | tojson }},
                        datasets: [{
                            label: 'Number of Patients',
                            data: {{ monthly_stats | map(attribute='PatientID') | list | tojson }},
                            borderColor: '#3498db',
                            fill: false
                        }, {
                            label: 'Average Length of Stay (days)',
                            data: {{ monthly_stats | map(attribute='LengthOfStay') | list | tojson }},
                            borderColor: '#2ecc71',
                            fill: false,
                            yAxisID: 'y1'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Monthly Statistics'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Number of Patients'
                                }
                            },
                            y1: {
                                beginAtZero: true,
                                position: 'right',
                                title: {
                                    display: true,
                                    text: 'Average Length of Stay (days)'
                                }
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
    
    def _get_custom_template(self) -> str:
        """Get the HTML template for custom report."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                /* Same base styles as summary template */
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #003d5c 0%, #0056b3 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .data-container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #f8f9fa;
                    font-weight: bold;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{ hospital_name }}</h1>
                <h2>{{ title }}</h2>
                <p>Generated on: {{ generated_at }}</p>
            </div>
            
            <div class="data-container">
                <table>
                    <thead>
                        <tr>
                            {% for key in data[0].keys() %}
                            <th>{{ key }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                        <tr>
                            {% for value in row.values() %}
                            <td>{{ value }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """ 