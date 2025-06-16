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
        self.selected_file = None
        
        # Create the UI
        self.create_widgets()
        
        # Center the window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
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
        """Handle file selection."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=os.path.basename(file_path))
            
            try:
                # Load data from the selected file
                self.data_processor.load_data(file_path, sheet_name=self.sheet_var.get())
                self.update_preview()
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.selected_file = None
                self.file_label.configure(text="No file selected")
    
    def update_preview(self):
        """Update the preview panel with data summary."""
        if self.data_processor.is_data_loaded():
            data = self.data_processor.get_data()
            summary = self.data_processor.get_summary()
            
            preview_text = f"Data Summary:\n\n"
            preview_text += f"Total Records: {summary['total_records']}\n"
            preview_text += f"Date Range: {summary['date_range']}\n"
            preview_text += f"Columns: {', '.join(summary['columns'])}\n"
            
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", preview_text)
    
    def generate_report(self):
        """Generate the report based on selected options."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an Excel file first!")
            return
        
        try:
            # Get report options
            report_type = self.report_type.get()
            date_range = self.date_range_var.get()
            output_format = self.output_var.get().lower()
            
            # Generate the report
            output_path = self.report_generator.generate_report(
                self.data_processor,
                report_type,
                date_range,
                output_format
            )
            
            if output_path:
                messagebox.showinfo("Success", f"Report generated successfully!\nSaved to: {output_path}")
                
                # Open the report if it's HTML
                if output_format == "html":
                    webbrowser.open(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

def main():
    """Main entry point for the application."""
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 