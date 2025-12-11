"""
Vercel serverless function entry point
"""

import sys
import os
from pathlib import Path
import traceback

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

# Set environment
os.environ.setdefault('DATABASE_URL', os.getenv('DATABASE_URL', 'sqlite:///./app.db'))
os.environ.setdefault('SECRET_KEY', os.getenv('SECRET_KEY', 'dev-key-change-production'))

try:
    # Import FastAPI app
    from app.main import app
    print(f"✓ FastAPI app loaded successfully")
except Exception as e:
    print(f"✗ Error loading FastAPI app: {e}")
    print(traceback.format_exc())
    
    # Create fallback app for debugging
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/health")
    @app.post("/health")
    async def health():
        return JSONResponse({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "env": {
                "DATABASE_URL": os.getenv('DATABASE_URL', 'not set'),
                "SECRET_KEY": "***" if os.getenv('SECRET_KEY') else "not set"
            }
        })

# Export for Vercel ASGI
__all__ = ['app']


