#!/usr/bin/env python3
"""
Main application entry point for IIIT Dharwad Timetable Scheduler.

This file provides a convenient way to run the FastAPI server directly
from the project root directory.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from timetable_scheduler.api.main import app
    import uvicorn
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you've installed the project dependencies:")
    print("  pip install -r requirements.txt")
    print("  pip install -e .")
    sys.exit(1)


def main():
    """Main entry point for the application."""
    print("🚀 Starting IIIT Dharwad Timetable Scheduler API...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔄 Interactive API docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()