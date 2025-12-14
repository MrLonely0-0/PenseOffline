"""
Vercel serverless function entry point
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

# Set environment
os.environ.setdefault('DATABASE_URL', os.getenv('DATABASE_URL', 'sqlite:///./app.db'))
os.environ.setdefault('SECRET_KEY', os.getenv('SECRET_KEY', 'dev-key-change-production'))

# Import FastAPI app
from app.main import app

# Vercel expects 'app' or a handler function
# For ASGI apps like FastAPI, we export the app directly
handler = app


