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
os.environ.setdefault('DATABASE_URL', 'sqlite:///./app.db')
os.environ.setdefault('SECRET_KEY', 'dev-key-change-production')

# Import FastAPI app
from app.main import app

# Export for Vercel ASGI
__all__ = ['app']


