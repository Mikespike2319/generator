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
        
        # File selection
        self.file_frame = ctk.CTkFrame(self.content_frame)
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
        
        # Report options
        self.options_frame = ctk.CTkFrame(self.content_frame)
        self.options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Report type selection
        self.report_type_label = ctk.CTkLabel(
            self.options_frame,
            text="Select Report Type:",
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
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            self.content_frame,
            text="Generate Report",
            command=self.generate_report,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.generate_btn.grid(row=2, column=0, padx=20, pady=20)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data_processor.load_data(file_path)
                self.file_label.configure(text=f"File: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Excel file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")
    
    def generate_report(self):
        if not self.data_processor.has_data():
            messagebox.showerror("Error", "Please select an Excel file first!")
            return
            
        try:
            report_type = self.report_type.get()
            report_content = self.report_generator.generate_report(
                self.data_processor.get_data(),
                report_type
            )
            
            # Save HTML file
            output_file = f"hospital_report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # Open the HTML file in default browser
            webbrowser.open(f'file://{os.path.abspath(output_file)}')
            
            messagebox.showinfo("Success", f"Report generated successfully!\nFile: {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 