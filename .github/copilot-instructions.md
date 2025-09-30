<!-- Project-specific instructions for GitHub Copilot -->

# IIIT Dharwad Automatic Timetable Scheduling System

## Project Overview
This is a Python-based automatic timetable scheduling system designed specifically for IIIT Dharwad. The system uses constraint satisfaction algorithms and optimization techniques to generate optimal class schedules.

## Architecture Guidelines
- Follow MVC (Model-View-Controller) pattern
- Use modular design with separate concerns
- Implement proper error handling and logging
- Follow PEP 8 style guidelines
- Use type hints for better code documentation

## Key Components
- **Models**: Data structures for courses, professors, rooms, time slots
- **Schedulers**: Core scheduling algorithms (genetic algorithm, constraint satisfaction)
- **Validators**: Constraint checking and validation logic
- **Utils**: Helper functions and utilities
- **API**: RESTful API endpoints for frontend integration
- **CLI**: Command-line interface for batch operations

## Coding Standards
- Use descriptive variable and function names
- Add docstrings to all classes and functions
- Implement proper exception handling
- Write unit tests for all core functionality
- Use logging instead of print statements

## Dependencies
- Core: Python 3.9+
- Optimization: DEAP, OR-Tools
- Web Framework: FastAPI or Flask
- Database: SQLAlchemy with SQLite/PostgreSQL
- Testing: pytest
- Utilities: pandas, numpy

✅ **Step 1: Clarify Project Requirements** - COMPLETED
✅ **Step 2: Scaffold the Project** - COMPLETED

## Project Structure Created

The Python project has been successfully scaffolded with the following structure:

### Core Modules
- **Models**: Course, Professor, Room, TimeSlot, Schedule, Constraint, Assignment
- **Schedulers**: Base scheduler interface with genetic and constraint satisfaction algorithms  
- **Validators**: Constraint validation and schedule verification
- **Utils**: Configuration loader, logging, data validation, export utilities
- **API**: REST API endpoints for web integration
- **CLI**: Command-line interface for batch operations

### Configuration
- **pyproject.toml**: Modern Python project configuration
- **requirements.txt**: Production dependencies  
- **requirements-dev.txt**: Development dependencies
- **config/**: YAML configuration files for system settings and constraints

### Testing & Documentation
- **tests/**: Complete test structure with fixtures and model tests
- **docs/**: Documentation directory with README
- **data/**: Sample data and templates

### Development Setup
- **LICENSE**: MIT license
- **.gitignore**: Comprehensive ignore patterns
- **README.md**: Detailed project documentation