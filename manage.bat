@echo off
SET PORT=8000

if /I "%1"=="start" goto start
if /I "%1"=="stop" goto stop
if /I "%1"=="restart" goto restart

echo Usage: manage.bat [start^|stop^|restart]
goto :EOF

:start
echo Starting FastAPI application on port %PORT%...
start "FastAPI_Backend" cmd /k "uvicorn main:app --port %PORT% --reload"
echo Application started in a new window.
goto :EOF

:stop
echo Stopping FastAPI application on port %PORT%...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":%PORT% " ^| find "LISTENING"') do (
    echo Killing process ID %%a...
    taskkill /F /PID %%a
)
echo Application stopped.
goto :EOF

:restart
call "%~0" stop
timeout /t 2 /nobreak >nul
call "%~0" start
goto :EOF
