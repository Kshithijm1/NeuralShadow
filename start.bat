@echo off
TITLE Neural Shadow System

echo ====================================================
echo   NEURAL SHADOW - STARTUP
echo ====================================================

echo Starting Backend (Python)...
start "Neural Shadow Backend" cmd /k "python main.py"

echo Waiting for backend...
timeout /t 5 /nobreak >nul

echo Starting Frontend (Next.js)...
cd web
start "Neural Shadow Interface" cmd /k "npm run dev"

echo ====================================================
echo   SYSTEM ONLINE
echo   - API: http://localhost:8000
echo   - UI:  http://localhost:3000
echo ====================================================
pause
