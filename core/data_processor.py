import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataProcessor:
    """Processes and analyzes data for report generation"""
    
    def __init__(self):
        self.data = None
        self.processed_data = {}
        
    def process_data(self, data, report_type="summary"):
        """
        Process data based on report type
        
        Args:
            data (pandas.DataFrame): Raw data
            report_type (str): Type of report to generate
            
        Returns:
            dict: Processed data ready for report generation
        """
        self.data = data.copy()
        
        # Basic data analysis
        basic_stats = self.get_basic_statistics()
        
        # Process based on report type
        if report_type == "summary":
            processed = self.process_summary_report()
        elif report_type == "detailed":
            processed = self.process_detailed_report()
        elif report_type == "overview":
            processed = self.process_overview_report()
        else:
            processed = self.process_summary_report()
            
        # Combine with basic stats
        processed.update(basic_stats)
        
        self.processed_data = processed
        return processed
        
    def get_basic_statistics(self):
        """Get basic statistics about the data"""
        stats = {
            'total_rows': len(self.data),
            'total_columns': len(self.data.columns),
            'column_names': list(self.data.columns),
            'data_types': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'numeric_columns': list(self.data.select_dtypes(include=[np.number]).columns),
            'text_columns': list(self.data.select_dtypes(include=['object']).columns),
            'datetime_columns': list(self.data.select_dtypes(include=['datetime64']).columns)
        }
        
        # Add numeric statistics
        if stats['numeric_columns']:
            numeric_data = self.data[stats['numeric_columns']]
            stats['numeric_stats'] = {
                'mean': numeric_data.mean().to_dict(),
                'median': numeric_data.median().to_dict(),
                'std': numeric_data.std().to_dict(),
                'min': numeric_data.min().to_dict(),
                'max': numeric_data.max().to_dict()
            }
        
        return stats
        
    def process_summary_report(self):
        """Process data for summary report"""
        summary = {
            'report_type': 'summary',
            'title': 'Data Summary Report',
            'sections': []
        }
        
        # Data overview section
        overview_section = {
            'title': 'Data Overview',
            'content': {
                'total_records': len(self.data),
                'total_fields': len(self.data.columns),
                'data_quality': self.assess_data_quality(),
                'top_values': self.get_top_values_per_column()
            }
        }
        summary['sections'].append(overview_section)
        
        # Numeric analysis section
        if self.data.select_dtypes(include=[np.number]).columns.any():
            numeric_section = {
                'title': 'Numeric Analysis',
                'content': self.analyze_numeric_data()
            }
            summary['sections'].append(numeric_section)
            
        # Text analysis section
        if self.data.select_dtypes(include=['object']).columns.any():
            text_section = {
                'title': 'Text Analysis',
                'content': self.analyze_text_data()
            }
            summary['sections'].append(text_section)
            
        return summary
        
    def process_detailed_report(self):
        """Process data for detailed report"""
        detailed = {
            'report_type': 'detailed',
            'title': 'Detailed Data Analysis',
            'sections': []
        }
        
        # Column-by-column analysis
        for column in self.data.columns:
            column_analysis = self.analyze_column(column)
            section = {
                'title': f'Column: {column}',
                'content': column_analysis
            }
            detailed['sections'].append(section)
            
        # Correlation analysis
        if len(self.data.select_dtypes(include=[np.number]).columns) > 1:
            correlation_section = {
                'title': 'Correlation Analysis',
                'content': self.analyze_correlations()
            }
            detailed['sections'].append(correlation_section)
            
        return detailed
        
    def process_overview_report(self):
        """Process data for overview report"""
        overview = {
            'report_type': 'overview',
            'title': 'Data Overview Report',
            'sections': []
        }
        
        # Quick stats section
        quick_stats = {
            'title': 'Quick Statistics',
            'content': {
                'shape': f"{len(self.data)} rows × {len(self.data.columns)} columns",
                'completeness': f"{((self.data.count().sum() / (len(self.data) * len(self.data.columns))) * 100):.1f}%",
                'unique_values': {col: self.data[col].nunique() for col in self.data.columns},
                'sample_data': self.data.head(10).to_dict('records')
            }
        }
        overview['sections'].append(quick_stats)
        
        # Data types section
        types_section = {
            'title': 'Data Types',
            'content': self.categorize_columns()
        }
        overview['sections'].append(types_section)
        
        return overview
        
    def assess_data_quality(self):
        """Assess overall data quality"""
        total_cells = len(self.data) * len(self.data.columns)
        missing_cells = self.data.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        quality = {
            'completeness_percentage': round(completeness, 2),
            'missing_values_count': int(missing_cells),
            'duplicate_rows': int(self.data.duplicated().sum()),
            'quality_score': self.calculate_quality_score()
        }
        
        return quality
        
    def calculate_quality_score(self):
        """Calculate a simple data quality score"""
        # Factors: completeness, uniqueness, consistency
        completeness = (1 - (self.data.isnull().sum().sum() / (len(self.data) * len(self.data.columns))))
        uniqueness = (1 - (self.data.duplicated().sum() / len(self.data)))
        
        # Simple average (can be made more sophisticated)
        score = (completeness + uniqueness) / 2 * 100
        return round(score, 1)
        
    def get_top_values_per_column(self, top_n=5):
        """Get top values for each column"""
        top_values = {}
        
        for column in self.data.columns:
            if self.data[column].dtype == 'object' or self.data[column].nunique() < 20:
                value_counts = self.data[column].value_counts().head(top_n)
                top_values[column] = value_counts.to_dict()
                
        return top_values
        
    def analyze_numeric_data(self):
        """Analyze numeric columns"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {'message': 'No numeric columns found'}
            
        analysis = {}
        
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            
            analysis[col] = {
                'count': len(col_data),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()),
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'quartiles': {
                    'q1': float(col_data.quantile(0.25)),
                    'q3': float(col_data.quantile(0.75))
                },
                'outliers_count': self.count_outliers(col_data)
            }
            
        return analysis
        
    def analyze_text_data(self):
        """Analyze text columns"""
        text_cols = self.data.select_dtypes(include=['object']).columns
        
        if len(text_cols) == 0:
            return {'message': 'No text columns found'}
            
        analysis = {}
        
        for col in text_cols:
            col_data = self.data[col].dropna().astype(str)
            
            analysis[col] = {
                'unique_count': self.data[col].nunique(),
                'most_common': self.data[col].value_counts().head(3).to_dict(),
                'avg_length': float(col_data.str.len().mean()),
                'contains_numbers': int(col_data.str.contains(r'\d').sum()),
                'contains_special_chars': int(col_data.str.contains(r'[^a-zA-Z0-9\s]').sum())
            }
            
        return analysis
        
    def analyze_column(self, column):
        """Detailed analysis of a single column"""
        col_data = self.data[column]
        
        analysis = {
            'data_type': str(col_data.dtype),
            'total_count': len(col_data),
            'non_null_count': col_data.count(),
            'null_count': col_data.isnull().sum(),
            'unique_count': col_data.nunique(),
            'null_percentage': (col_data.isnull().sum() / len(col_data)) * 100
        }
        
        # Type-specific analysis
        if pd.api.types.is_numeric_dtype(col_data):
            non_null_data = col_data.dropna()
            analysis.update({
                'mean': float(non_null_data.mean()),
                'median': float(non_null_data.median()),
                'std': float(non_null_data.std()),
                'min': float(non_null_data.min()),
                'max': float(non_null_data.max()),
                'range': float(non_null_data.max() - non_null_data.min())
            })
        elif pd.api.types.is_object_dtype(col_data):
            analysis.update({
                'most_frequent': col_data.mode().iloc[0] if not col_data.mode().empty else None,
                'top_values': col_data.value_counts().head(5).to_dict()
            })
            
        return analysis
        
    def analyze_correlations(self):
        """Analyze correlations between numeric columns"""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            return {'message': 'Need at least 2 numeric columns for correlation analysis'}
            
        correlation_matrix = numeric_data.corr()
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:  # Strong correlation threshold
                    strong_correlations.append({
                        'column1': correlation_matrix.columns[i],
                        'column2': correlation_matrix.columns[j],
                        'correlation': float(corr_value)
                    })
                    
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
        
    def categorize_columns(self):
        """Categorize columns by data type"""
        categories = {
            'numeric': list(self.data.select_dtypes(include=[np.number]).columns),
            'text': list(self.data.select_dtypes(include=['object']).columns),
            'datetime': list(self.data.select_dtypes(include=['datetime64']).columns),
            'boolean': list(self.data.select_dtypes(include=['bool']).columns)
        }
        
        # Add more specific categorization
        categories['categorical'] = []
        categories['continuous'] = []
        
        for col in categories['text']:
            if self.data[col].nunique() < 20:  # Likely categorical
                categories['categorical'].append(col)
                
        for col in categories['numeric']:
            if self.data[col].nunique() > 20:  # Likely continuous
                categories['continuous'].append(col)
                
        return categories
        
    def count_outliers(self, series):
        """Count outliers using IQR method"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return len(outliers)
        
    def sort_data(self, column, ascending=True):
        """Sort data by specified column"""
        if column in self.data.columns:
            return self.data.sort_values(by=column, ascending=ascending)
        else:
            raise ValueError(f"Column '{column}' not found in data")
            
    def filter_data(self, filters):
        """
        Filter data based on conditions
        
        Args:
            filters (dict): Dictionary of column: condition pairs
            
        Returns:
            pandas.DataFrame: Filtered data
        """
        filtered_data = self.data.copy()
        
        for column, condition in filters.items():
            if column in filtered_data.columns:
                # Simple string contains filter for now
                if isinstance(condition, str):
                    filtered_data = filtered_data[
                        filtered_data[column].astype(str).str.contains(condition, case=False, na=False)
                    ]
                    
        return filtered_data 