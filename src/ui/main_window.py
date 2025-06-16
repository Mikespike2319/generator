import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import webbrowser
from ..core.report_generator import ReportGenerator
from ..core.data_processor import DataProcessor
from ..utils.config_manager import ConfigManager

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config = ConfigManager()
        
        # Set up the window
        self.title("Hospital Report Generator")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize data
        self.data_processor = DataProcessor()
        self.report_generator = ReportGenerator()
        
        # Create the UI
        self.create_widgets()
        
    def create_widgets(self):
        # Create main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Hospital Report Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Left panel for file selection and options
        self.left_panel = ctk.CTkFrame(self.content_frame)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # File selection section
        self.file_frame = ctk.CTkFrame(self.left_panel)
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.file_label = ctk.CTkLabel(
            self.file_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12)
        )
        self.file_label.pack(side="left", padx=10)
        
        self.select_file_btn = ctk.CTkButton(
            self.file_frame,
            text="Select Excel File",
            command=self.select_file
        )
        self.select_file_btn.pack(side="right", padx=10)
        
        # Excel options section
        self.excel_options_frame = ctk.CTkFrame(self.left_panel)
        self.excel_options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.sheet_label = ctk.CTkLabel(
            self.excel_options_frame,
            text="Sheet Selection:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.sheet_label.pack(pady=(10, 5))
        
        self.sheet_var = ctk.StringVar(value="Sheet1")
        self.sheet_entry = ctk.CTkEntry(
            self.excel_options_frame,
            textvariable=self.sheet_var,
            placeholder_text="Enter sheet name"
        )
        self.sheet_entry.pack(pady=5)
        
        # Report options section
        self.options_frame = ctk.CTkFrame(self.left_panel)
        self.options_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.report_type_label = ctk.CTkLabel(
            self.options_frame,
            text="Report Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.report_type_label.pack(pady=(10, 5))
        
        self.report_type = ctk.StringVar(value="summary")
        
        report_types = [
            ("Summary Report", "summary"),
            ("Patient Demographics", "demographics"),
            ("Department Analysis", "department"),
            ("Monthly Statistics", "monthly"),
            ("Custom Query", "custom")
        ]
        
        for text, value in report_types:
            ctk.CTkRadioButton(
                self.options_frame,
                text=text,
                variable=self.report_type,
                value=value
            ).pack(pady=5)
        
        # Report customization section
        self.customization_frame = ctk.CTkFrame(self.left_panel)
        self.customization_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        self.customization_label = ctk.CTkLabel(
            self.customization_frame,
            text="Report Customization:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.customization_label.pack(pady=(10, 5))
        
        # Date range selection
        self.date_range_frame = ctk.CTkFrame(self.customization_frame)
        self.date_range_frame.pack(fill="x", padx=10, pady=5)
        
        self.date_range_label = ctk.CTkLabel(
            self.date_range_frame,
            text="Date Range:"
        )
        self.date_range_label.pack(side="left", padx=5)
        
        self.date_range_var = ctk.StringVar(value="all")
        self.date_range_combo = ctk.CTkComboBox(
            self.date_range_frame,
            values=["All Time", "Last Month", "Last 3 Months", "Last 6 Months", "Last Year"],
            variable=self.date_range_var
        )
        self.date_range_combo.pack(side="right", padx=5)
        
        # Output options
        self.output_frame = ctk.CTkFrame(self.customization_frame)
        self.output_frame.pack(fill="x", padx=10, pady=5)
        
        self.output_label = ctk.CTkLabel(
            self.output_frame,
            text="Output Format:"
        )
        self.output_label.pack(side="left", padx=5)
        
        self.output_var = ctk.StringVar(value="html")
        self.output_combo = ctk.CTkComboBox(
            self.output_frame,
            values=["HTML", "PDF", "Excel"],
            variable=self.output_var
        )
        self.output_combo.pack(side="right", padx=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            self.left_panel,
            text="Generate Report",
            command=self.generate_report,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.generate_btn.grid(row=4, column=0, padx=20, pady=20)
        
        # Right panel for preview
        self.right_panel = ctk.CTkFrame(self.content_frame)
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        self.preview_label = ctk.CTkLabel(
            self.right_panel,
            text="Report Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.preview_label.pack(pady=10)
        
        self.preview_text = ctk.CTkTextbox(
            self.right_panel,
            width=400,
            height=600
        )
        self.preview_text.pack(padx=10, pady=10, fill="both", expand=True)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data_processor.load_data(file_path, sheet_name=self.sheet_var.get())
                self.file_label.configure(text=f"File: {os.path.basename(file_path)}")
                self.update_preview()
                messagebox.showinfo("Success", "Excel file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")
    
    def update_preview(self):
        """Update the preview panel with data summary."""
        if self.data_processor.has_data():
            data = self.data_processor.get_data()
            preview_text = f"Data Summary:\n\n"
            preview_text += f"Total Rows: {len(data)}\n"
            preview_text += f"Columns: {', '.join(data.columns)}\n"
            preview_text += f"\nFirst few rows:\n{data.head().to_string()}"
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", preview_text)
    
    def generate_report(self):
        if not self.data_processor.has_data():
            messagebox.showerror("Error", "Please select an Excel file first!")
            return
            
        try:
            report_type = self.report_type.get()
            output_format = self.output_var.get().lower()
            date_range = self.date_range_var.get()
            
            # Get data and apply date range filter if needed
            data = self.data_processor.get_data()
            if date_range != "All Time":
                # Apply date filtering logic here
                pass
            
            report_content = self.report_generator.generate_report(
                data,
                report_type,
                output_format=output_format
            )
            
            # Save file based on output format
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if output_format == 'html':
                output_file = f"hospital_report_{report_type}_{timestamp}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                webbrowser.open(f'file://{os.path.abspath(output_file)}')
            elif output_format == 'pdf':
                output_file = f"hospital_report_{report_type}_{timestamp}.pdf"
                # Add PDF generation logic
                pass
            elif output_format == 'excel':
                output_file = f"hospital_report_{report_type}_{timestamp}.xlsx"
                # Add Excel generation logic
                pass
            
            messagebox.showinfo("Success", f"Report generated successfully!\nFile: {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 