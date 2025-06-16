from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hospital_report_generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional desktop application for generating hospital reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hospital_report_generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "openpyxl>=3.1.0",
        "customtkinter>=5.2.0",
        "pillow>=10.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hospital-report-generator=src.main:main",
        ],
    },
) 