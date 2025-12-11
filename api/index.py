"""
Vercel serverless function entry point for FastAPI backend
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Set environment defaults
os.environ.setdefault('DATABASE_URL', 'sqlite:///./app.db')
os.environ.setdefault('SECRET_KEY', 'dev-key-change-in-production')
os.environ.setdefault('PYTHONPATH', backend_path)

# Import FastAPI app
try:
    from app.main import app
    print(f"✓ FastAPI app loaded successfully from {backend_path}/app/main.py")
except ImportError as e:
    print(f"✗ Error importing app.main: {e}")
    print(f"  Python path: {sys.path}")
    print(f"  Current directory: {os.getcwd()}")
    
    # Fallback: simple app for debugging
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/health")
    async def health():
        return JSONResponse({
            "status": "error",
            "message": f"Failed to load FastAPI app: {str(e)}",
            "sys_path": sys.path,
            "cwd": os.getcwd(),
            "backend_path": backend_path
        })
    
    @app.get("/")
    async def root():
        return JSONResponse({"error": str(e)})

# Vercel will call this ASGI app

