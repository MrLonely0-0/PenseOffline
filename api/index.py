"""
Vercel serverless function that runs the FastAPI backend
This file acts as the entry point for all /api/* routes on Vercel
"""

import sys
from pathlib import Path

# Add backend directory to path so imports work
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import and expose the FastAPI app
from app.main import app

# Vercel requires the app to be exported as 'app' for serverless
