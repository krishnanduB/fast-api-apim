@echo off
SET PORT=8000
echo Stopping FastAPI application on port %PORT%...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":%PORT% " ^| find "LISTENING"') do (
    echo Killing process ID %%a...
    taskkill /F /PID %%a
)
echo Application stopped.
