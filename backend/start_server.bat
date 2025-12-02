@echo off
set PORT=8000
if NOT "%1"=="" set PORT=%1
if not exist .venv (
  echo [start] Creating virtual environment...
  python -m venv .venv
)
call .\.venv\Scripts\activate
echo [start] Installing dependencies (quiet)...
pip install -r requirements.txt > nul
echo [start] Starting server on port %PORT%
python -m uvicorn app.main:app --reload --port %PORT%
