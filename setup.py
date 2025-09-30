#!/usr/bin/env python
"""
Setup script for IIIT Dharwad Automatic Timetable Scheduling System.

This setup.py file is provided for backward compatibility.
The main project configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
def read_requirements(filename):
    """Read requirements from a requirements file."""
    requirements_path = this_directory / filename
    if requirements_path.exists():
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Main requirements
install_requires = read_requirements('requirements.txt')

# Development requirements
dev_requires = read_requirements('requirements-dev.txt')

setup(
    name="timetable-scheduler",
    version="0.1.0",
    
    # Author and contact information
    author="IIIT Dharwad",
    author_email="contact@iiitdharwad.edu.in",
    
    # Project description
    description="IIIT Dharwad Automatic Timetable Scheduling System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Project URLs
    url="https://github.com/iiitdharwad/timetable-scheduler",
    project_urls={
        "Bug Tracker": "https://github.com/iiitdharwad/timetable-scheduler/issues",
        "Documentation": "https://timetable-scheduler.readthedocs.io/",
        "Source Code": "https://github.com/iiitdharwad/timetable-scheduler",
    },
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Dependencies
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
    },
    
    # Python version requirement
    python_requires=">=3.9",
    
    # Package metadata
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # Keywords
    keywords="timetable scheduling optimization education university college",
    
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "timetable-scheduler=timetable_scheduler.cli.main:main",
        ],
    },
    
    # Include additional files
    include_package_data=True,
    package_data={
        "timetable_scheduler": [
            "py.typed",  # Indicates this package supports typing
        ],
    },
    
    # Zip safe
    zip_safe=False,
    
    # License
    license="MIT",
    
    # Additional metadata
    platforms=["any"],
    
    # Test suite configuration
    test_suite="tests",
    tests_require=[
        "pytest>=6.0.0",
        "pytest-cov>=2.12.0",
        "pytest-asyncio>=0.15.0",
    ],
)