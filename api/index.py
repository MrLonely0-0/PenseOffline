"""
Vercel serverless function entry point for FastAPI backend
Routes /api/* to the FastAPI application
"""

import sys
import os
from pathlib import Path

# Set Python path to include backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set required environment variables
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./app.db'

if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'dev-key-change-in-production'

try:
    from app.main import app
except ImportError as e:
    print(f"Error importing FastAPI app: {e}")
    # Fallback app for debugging
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/health")
    def health():
        return {"status": "error", "message": str(e)}

# Export the app as a ASGI application for Vercel
# Vercel will automatically detect this as a Python ASGI app
