"""
Simple app.py entry point for the FastAPI application.

This is a common convention where app.py serves as the main entry point.
The actual FastAPI app is defined in main.py for better organization.
"""

from .main import app

# Re-export the app for convenience
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)