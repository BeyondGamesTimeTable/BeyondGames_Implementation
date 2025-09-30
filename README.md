# IIIT Dharwad Automatic Timetable Scheduling System

An intelligent timetable scheduling system designed specifically for IIIT Dharwad that uses advanced algorithms to generate optimal class schedules while respecting various constraints.

## Features

- **Constraint-Based Scheduling**: Handles complex scheduling constraints including room availability, professor schedules, and course requirements
- **Multiple Algorithm Support**: Implements genetic algorithms, constraint satisfaction, and optimization techniques
- **RESTful API**: Web-based interface for easy integration
- **Command Line Interface**: Batch processing capabilities
- **Comprehensive Validation**: Ensures schedule feasibility and optimization
- **Flexible Configuration**: Easy customization for different academic terms and requirements

## Project Structure

```
src/
├── timetable_scheduler/
│   ├── models/          # Data models (Course, Professor, Room, TimeSlot)
│   ├── schedulers/      # Core scheduling algorithms
│   ├── validators/      # Constraint validation logic
│   ├── utils/           # Helper functions and utilities
│   ├── api/             # REST API endpoints
│   └── cli/             # Command-line interface
tests/                   # Unit and integration tests
docs/                    # Documentation
config/                  # Configuration files
data/                    # Sample data and templates
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "Automated TimeTable Scheduling BeyondGames"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Install the package in development mode:
```bash
pip install -e .
```

## Usage

### Command Line Interface
```bash
# Generate a basic timetable
python -m timetable_scheduler.cli generate --input data/sample_input.json --output schedule.json

# Validate an existing schedule
python -m timetable_scheduler.cli validate --schedule schedule.json
```

### API Server
```bash
# Start the development server
python -m timetable_scheduler.api.server

# Access the API documentation at http://localhost:8000/docs
```

### Python Library
```python
from timetable_scheduler import TimetableScheduler
from timetable_scheduler.models import Course, Professor, Room

# Create scheduler instance
scheduler = TimetableScheduler()

# Load your data
courses = [...]  # Load course data
professors = [...]  # Load professor data
rooms = [...]  # Load room data

# Generate schedule
schedule = scheduler.generate_schedule(courses, professors, rooms)
```

## Configuration

The system uses configuration files in the `config/` directory:
- `default.yaml`: Default system settings
- `constraints.yaml`: Scheduling constraints and rules
- `optimization.yaml`: Algorithm parameters and weights

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src/timetable_scheduler --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact the development team at IIIT Dharwad.