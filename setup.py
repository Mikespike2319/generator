from setuptools import setup, find_packages

setup(
    name="hospital_report_generator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "customtkinter>=5.2.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "jinja2>=3.1.0",
        "pdfkit>=1.0.0",
        "wkhtmltopdf>=0.2"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "hospital_report_generator=hospital_report_generator.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern Python application for generating hospital reports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 