import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path
import webbrowser

from core.excel_handler import ExcelHandler
from core.data_processor import DataProcessor
from core.report_generator import ReportGenerator

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Excel Data Analysis Report Generator")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Initialize components
        self.excel_handler = ExcelHandler()
        self.data_processor = DataProcessor()
        self.report_generator = ReportGenerator()
        
        # Variables
        self.selected_file = None
        self.processed_data = None
        
        # Create UI
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create and layout all widgets"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Footer
        self.create_footer()
        
    def create_header(self):
        """Create header section"""
        header_frame = ctk.CTkFrame(self, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Excel Data Analysis Report Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(expand=True)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Transform your Excel data into professional analysis reports",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
    def create_main_content(self):
        """Create main content area"""
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Right panel - Preview
        self.create_preview_panel(main_frame)
        
    def create_control_panel(self, parent):
        """Create control panel"""
        control_frame = ctk.CTkFrame(parent, width=350)
        control_frame.grid(row=0, column=0, sticky="ns", padx=(20, 10), pady=20)
        control_frame.grid_propagate(False)
        
        # File selection section
        file_section = ctk.CTkFrame(control_frame)
        file_section.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            file_section,
            text="📁 Select Excel File",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        self.file_label = ctk.CTkLabel(
            file_section,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.file_label.pack(pady=(0, 10))
        
        self.select_button = ctk.CTkButton(
            file_section,
            text="Browse Files",
            command=self.select_file,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.select_button.pack(pady=(0, 15))
        
        # Processing options section
        options_section = ctk.CTkFrame(control_frame)
        options_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            options_section,
            text="⚙️ Report Options",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Report type selection
        self.report_type = ctk.StringVar(value="summary")
        
        ctk.CTkLabel(options_section, text="Report Type:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15)
        
        report_frame = ctk.CTkFrame(options_section)
        report_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        ctk.CTkRadioButton(
            report_frame, text="Summary Report", 
            variable=self.report_type, value="summary"
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkRadioButton(
            report_frame, text="Detailed Analysis", 
            variable=self.report_type, value="detailed"
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkRadioButton(
            report_frame, text="Data Overview", 
            variable=self.report_type, value="overview"
        ).pack(anchor="w", padx=10, pady=2)
        
        # Include charts option
        self.include_charts = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            options_section,
            text="Include Charts and Graphs",
            variable=self.include_charts
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Generate button
        self.generate_button = ctk.CTkButton(
            control_frame,
            text="🚀 Generate Report",
            command=self.generate_report,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.generate_button.pack(fill="x", padx=20, pady=20)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(control_frame)
        self.progress.pack(fill="x", padx=20, pady=(0, 20))
        self.progress.set(0)
        
    def create_preview_panel(self, parent):
        """Create preview panel"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            preview_frame,
            text="📊 Data Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(20, 10))
        
        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.preview_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Initially show welcome message
        welcome_text = """Welcome to Excel Data Analysis Report Generator!

Steps to get started:
1. Click 'Browse Files' to select your Excel file
2. Choose your report type and analysis options
3. Click 'Generate Report' to create your professional report

Supported formats: .xlsx, .xls
The generated report will automatically open in your browser with:
• Data quality assessment
• Statistical analysis
• Visual charts and graphs
• Professional formatting optimized for printing"""
        
        self.preview_text.insert("1.0", welcome_text)
        self.preview_text.configure(state="disabled")
        
    def create_footer(self):
        """Create footer section"""
        footer_frame = ctk.CTkFrame(self, height=50)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        footer_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Ready to process Excel files",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(expand=True)
        
    def select_file(self):
        """Handle file selection"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.configure(text=filename)
            self.status_label.configure(text=f"Selected: {filename}")
            
            # Load and preview data
            self.load_data_preview()
            
    def load_data_preview(self):
        """Load and display data preview"""
        try:
            self.status_label.configure(text="Loading data preview...")
            
            # Load data using excel handler
            data = self.excel_handler.load_file(self.selected_file)
            
            if data is not None:
                # Generate preview text
                preview = self.generate_preview_text(data)
                
                # Update preview
                self.preview_text.configure(state="normal")
                self.preview_text.delete("1.0", "end")
                self.preview_text.insert("1.0", preview)
                self.preview_text.configure(state="disabled")
                
                # Enable generate button
                self.generate_button.configure(state="normal")
                self.status_label.configure(text="File loaded successfully - Ready to generate report")
            else:
                raise Exception("Failed to load data")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_label.configure(text="Error loading file")
            
    def generate_preview_text(self, data):
        """Generate preview text from data"""
        preview = f"📋 File Information:\n"
        preview += f"Rows: {len(data)}\n"
        preview += f"Columns: {len(data.columns)}\n\n"
        
        preview += f"📊 Column Names:\n"
        for i, col in enumerate(data.columns[:10], 1):  # Show first 10 columns
            preview += f"{i}. {col}\n"
        if len(data.columns) > 10:
            preview += f"... and {len(data.columns) - 10} more columns\n"
            
        preview += f"\n🔍 Sample Data (first 5 rows):\n"
        preview += data.head().to_string()
        
        return preview
        
    def generate_report(self):
        """Generate HTML report"""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an Excel file first!")
            return
            
        # Run generation in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._generate_report_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_report_thread(self):
        """Generate report in separate thread"""
        try:
            # Update UI
            self.after(0, lambda: self.generate_button.configure(state="disabled", text="Generating..."))
            self.after(0, lambda: self.status_label.configure(text="Processing data..."))
            self.after(0, lambda: self.progress.set(0.2))
            
            # Load data
            data = self.excel_handler.load_file(self.selected_file)
            self.after(0, lambda: self.progress.set(0.4))
            
            # Process data
            processed_data = self.data_processor.process_data(
                data, 
                report_type=self.report_type.get()
            )
            self.after(0, lambda: self.progress.set(0.6))
            
            # Generate report
            report_path = self.report_generator.generate_html_report(
                processed_data,
                report_type=self.report_type.get(),
                include_charts=self.include_charts.get(),
                source_file=os.path.basename(self.selected_file)
            )
            self.after(0, lambda: self.progress.set(0.8))
            
            # Complete
            self.after(0, lambda: self.progress.set(1.0))
            self.after(0, lambda: self._report_generated_success(report_path))
            
        except Exception as e:
            self.after(0, lambda: self._report_generated_error(str(e)))
            
    def _report_generated_success(self, report_path):
        """Handle successful report generation"""
        self.generate_button.configure(state="normal", text="🚀 Generate Report")
        self.status_label.configure(text=f"Report generated successfully!")
        
        # Show success message
        result = messagebox.askyesno(
            "Success", 
            f"Report generated successfully!\n\nSaved to: {report_path}\n\nWould you like to open it now?"
        )
        
        if result:
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
            
        self.progress.set(0)
        
    def _report_generated_error(self, error_msg):
        """Handle report generation error"""
        self.generate_button.configure(state="normal", text="🚀 Generate Report")
        self.status_label.configure(text="Error generating report")
        self.progress.set(0)
        
        messagebox.showerror("Error", f"Failed to generate report:\n{error_msg}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 