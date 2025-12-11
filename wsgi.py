"""
WSGI entry point for Vercel
This file serves as the main entry point for all requests
"""

import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'sqlite:///./app.db')
os.environ.setdefault('SECRET_KEY', 'dev-key-change-in-production')

# Import the FastAPI app
from app.main import app

# Wrap FastAPI app for WSGI compatibility
from fastapi.middleware.wsgi import WSGIMiddleware

# This is the WSGI application that Vercel will call
