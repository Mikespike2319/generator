import os
import json
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from jinja2 import Environment, FileSystemLoader, Template

class ReportGenerator:
    """Generates HTML reports from processed data"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path("reports")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create template if it doesn't exist
        if not (self.template_dir / "report_template.html").exists():
            self.create_simple_template()
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
        
        # Configure matplotlib for better charts
        plt.style.use('default')
        
    def generate_html_report(self, processed_data, report_type="summary", 
                           include_charts=True, source_file=""):
        """
        Generate HTML report from processed data
        
        Args:
            processed_data (dict): Processed data from DataProcessor
            report_type (str): Type of report
            include_charts (bool): Whether to include charts
            source_file (str): Name of source Excel file
            
        Returns:
            str: Path to generated HTML file
        """
        # Generate charts if requested
        charts = {}
        if include_charts:
            charts = self.generate_charts(processed_data)
            
        # Prepare template context
        context = {
            'title': processed_data.get('title', 'Data Report'),
            'report_type': report_type,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_file': source_file,
            'data': processed_data,
            'charts': charts,
            'include_charts': include_charts
        }
        
        # Load and render template
        template = self.env.get_template('report_template.html')
        html_content = template.render(context)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{report_type}_{timestamp}.html"
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return str(output_path)
        
    def generate_charts(self, processed_data):
        """Generate charts from processed data"""
        charts = {}
        
        try:
            # Chart 1: Data completeness
            if 'missing_values' in processed_data:
                charts['completeness'] = self.create_completeness_chart(processed_data)
                
            # Chart 2: Data types distribution
            if 'data_types' in processed_data:
                charts['data_types'] = self.create_data_types_chart(processed_data)
                
            # Chart 3: Numeric distributions
            if 'numeric_stats' in processed_data and processed_data['numeric_stats']:
                charts['numeric_distributions'] = self.create_numeric_charts(processed_data)
                
            # Chart 4: Top values for categorical columns
            if 'sections' in processed_data:
                for section in processed_data['sections']:
                    if section['title'] == 'Data Overview' and 'top_values' in section['content']:
                        charts['top_values'] = self.create_top_values_chart(section['content']['top_values'])
                        break
                        
        except Exception as e:
            print(f"Error generating charts: {e}")
            
        return charts
        
    def create_completeness_chart(self, data):
        """Create data completeness chart"""
        try:
            missing_values = data['missing_values']
            total_rows = data['total_rows']
            
            # Calculate completeness percentages
            completeness = {}
            for col, missing in missing_values.items():
                completeness[col] = ((total_rows - missing) / total_rows) * 100
                
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            columns = list(completeness.keys())[:10]  # Limit to 10 columns
            values = [completeness[col] for col in columns]
            
            bars = ax.bar(columns, values, color='skyblue', alpha=0.7)
            ax.set_title('Data Completeness by Column', fontsize=16, fontweight='bold')
            ax.set_ylabel('Completeness (%)', fontsize=12)
            ax.set_xlabel('Columns', fontsize=12)
            ax.set_ylim(0, 100)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       f'{value:.1f}%', ha='center', va='bottom')
                       
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            return self.fig_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating completeness chart: {e}")
            return None
            
    def create_data_types_chart(self, data):
        """Create data types distribution chart"""
        try:
            data_types = data['data_types']
            
            # Count data types
            type_counts = {}
            for col, dtype in data_types.items():
                dtype_str = str(dtype)
                if 'int' in dtype_str or 'float' in dtype_str:
                    type_name = 'Numeric'
                elif 'object' in dtype_str:
                    type_name = 'Text'
                elif 'datetime' in dtype_str:
                    type_name = 'DateTime'
                elif 'bool' in dtype_str:
                    type_name = 'Boolean'
                else:
                    type_name = 'Other'
                    
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
                
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            wedges, texts, autotexts = ax.pie(
                type_counts.values(), 
                labels=type_counts.keys(),
                autopct='%1.1f%%',
                colors=colors[:len(type_counts)],
                startangle=90
            )
            
            ax.set_title('Data Types Distribution', fontsize=16, fontweight='bold')
            
            return self.fig_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating data types chart: {e}")
            return None
            
    def create_numeric_charts(self, data):
        """Create charts for numeric data"""
        try:
            numeric_stats = data['numeric_stats']
            
            if not numeric_stats or 'mean' not in numeric_stats:
                return None
                
            # Create subplots for mean, median, std
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Numeric Data Analysis', fontsize=16, fontweight='bold')
            
            # Mean values
            cols = list(numeric_stats['mean'].keys())[:8]  # Limit columns
            means = [numeric_stats['mean'][col] for col in cols]
            
            axes[0, 0].bar(cols, means, color='lightcoral', alpha=0.7)
            axes[0, 0].set_title('Mean Values')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Median values
            medians = [numeric_stats['median'][col] for col in cols]
            axes[0, 1].bar(cols, medians, color='lightblue', alpha=0.7)
            axes[0, 1].set_title('Median Values')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Standard deviation
            stds = [numeric_stats['std'][col] for col in cols]
            axes[1, 0].bar(cols, stds, color='lightgreen', alpha=0.7)
            axes[1, 0].set_title('Standard Deviation')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Min-Max range
            mins = [numeric_stats['min'][col] for col in cols]
            maxs = [numeric_stats['max'][col] for col in cols]
            ranges = [maxs[i] - mins[i] for i in range(len(cols))]
            
            axes[1, 1].bar(cols, ranges, color='gold', alpha=0.7)
            axes[1, 1].set_title('Value Ranges (Max - Min)')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            return self.fig_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating numeric charts: {e}")
            return None
            
    def create_top_values_chart(self, top_values_data):
        """Create chart showing top values for categorical columns"""
        try:
            if not top_values_data:
                return None
                
            # Select first few categorical columns
            columns_to_plot = list(top_values_data.keys())[:4]
            
            if not columns_to_plot:
                return None
                
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Top Values in Categorical Columns', fontsize=16, fontweight='bold')
            
            axes = axes.flatten()
            
            for i, col in enumerate(columns_to_plot):
                if i >= 4:
                    break
                    
                values = top_values_data[col]
                
                # Create horizontal bar chart
                y_pos = range(len(values))
                axes[i].barh(y_pos, list(values.values()), color=f'C{i}', alpha=0.7)
                axes[i].set_yticks(y_pos)
                axes[i].set_yticklabels(list(values.keys()))
                axes[i].set_title(f'Top Values: {col}')
                axes[i].set_xlabel('Count')
                
            # Hide unused subplots
            for i in range(len(columns_to_plot), 4):
                axes[i].set_visible(False)
                
            plt.tight_layout()
            
            return self.fig_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating top values chart: {e}")
            return None
            
    def fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        try:
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close(fig)  # Close figure to free memory
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            print(f"Error converting figure to base64: {e}")
            plt.close(fig)
            return None
            
    def create_simple_template(self):
        """Create a simple HTML template"""
        template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #007acc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #007acc;
            margin: 0;
            font-size: 2.5em;
        }
        .meta-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #333;
            border-left: 4px solid #007acc;
            padding-left: 15px;
            margin-bottom: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #dee2e6;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #007acc;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .chart-container {
            text-align: center;
            margin: 30px 0;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <p>Generated on {{ generated_at }}</p>
            {% if source_file %}
            <p><strong>Source:</strong> {{ source_file }}</p>
            {% endif %}
        </div>

        <div class="meta-info">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ data.total_rows }}</div>
                    <div class="stat-label">Total Rows</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ data.total_columns }}</div>
                    <div class="stat-label">Total Columns</div>
                </div>
            </div>
        </div>

        {% if include_charts and charts %}
        <div class="section">
            <h2>📊 Visual Analysis</h2>
            
            {% if charts.completeness %}
            <div class="chart-container">
                <h3>Data Completeness</h3>
                <img src="{{ charts.completeness }}" alt="Data Completeness Chart">
            </div>
            {% endif %}
            
            {% if charts.data_types %}
            <div class="chart-container">
                <h3>Data Types Distribution</h3>
                <img src="{{ charts.data_types }}" alt="Data Types Chart">
            </div>
            {% endif %}
        </div>
        {% endif %}

        {% if data.sections %}
        {% for section in data.sections %}
        <div class="section">
            <h2>{{ section.title }}</h2>
            
            {% if section.title == 'Data Overview' %}
                <p><strong>Total Records:</strong> {{ section.content.total_records }}</p>
                <p><strong>Total Fields:</strong> {{ section.content.total_fields }}</p>
                
                {% if section.content.data_quality %}
                <h3>Data Quality Assessment</h3>
                <ul>
                    <li>Completeness: {{ section.content.data_quality.completeness_percentage }}%</li>
                    <li>Missing Values: {{ section.content.data_quality.missing_values_count }}</li>
                    <li>Duplicate Rows: {{ section.content.data_quality.duplicate_rows }}</li>
                    <li>Overall Quality Score: {{ section.content.data_quality.quality_score }}/100</li>
                </ul>
                {% endif %}
                
            {% elif section.title == 'Numeric Analysis' %}
                {% for col, stats in section.content.items() %}
                {% if stats is mapping %}
                <h3>{{ col }}</h3>
                <ul>
                    <li>Count: {{ stats.count }}</li>
                    <li>Mean: {{ "%.2f"|format(stats.mean) }}</li>
                    <li>Median: {{ "%.2f"|format(stats.median) }}</li>
                    <li>Min: {{ "%.2f"|format(stats.min) }}</li>
                    <li>Max: {{ "%.2f"|format(stats.max) }}</li>
                </ul>
                {% endif %}
                {% endfor %}
                
            {% elif section.title == 'Text Analysis' %}
                {% for col, stats in section.content.items() %}
                {% if stats is mapping %}
                <h3>{{ col }}</h3>
                <ul>
                    <li>Unique Values: {{ stats.unique_count }}</li>
                    <li>Average Length: {{ "%.1f"|format(stats.avg_length) }}</li>
                </ul>
                {% endif %}
                {% endfor %}
            {% endif %}
        </div>
        {% endfor %}
        {% endif %}

        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p>Report generated by Excel to HTML Report Generator</p>
        </div>
    </div>
</body>
</html>'''
        
        # Ensure template directory exists
        self.template_dir.mkdir(exist_ok=True)
        
        # Write template file
        template_path = self.template_dir / "report_template.html"
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
            
        return str(template_path) 