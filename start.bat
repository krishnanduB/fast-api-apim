@echo off
SET PORT=8000
echo Installing dependencies...
pip install -r requirements.txt
echo Starting FastAPI application on port %PORT%...
start "FastAPI_Backend" cmd /k "uvicorn main:app --port %PORT% --reload"
echo Application started in a new window.
