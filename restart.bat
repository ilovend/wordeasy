@echo off
chcp 65001 > nul
echo ====================================
echo Restarting WordEasy Services...
echo ====================================

echo.
echo [1/3] Stopping existing processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Frontend*" 2>nul
timeout /t 2 /nobreak > nul

echo [2/3] Cleaning up ports...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173"') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak > nul

echo [3/3] Starting services...
cd /d "%~dp0"
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak > nul
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Services restarted successfully!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Please refresh your browser (Ctrl+F5)
echo ====================================
pause
