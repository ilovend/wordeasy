@echo off
chcp 65001 > nul
echo ====================================
echo WordEasy Service Diagnostics
echo ====================================
echo.

echo [Checking Port Usage]
echo Port 8000 (Backend):
netstat -ano | findstr ":8000"
echo.
echo Port 5173 (Frontend):
netstat -ano | findstr ":5173"
echo.

echo [Testing Backend API]
curl -s http://localhost:8000/api/progress
echo.
echo.

echo [Backend Processes]
tasklist | findstr python.exe
echo.

echo [Frontend Processes]
tasklist | findstr node.exe
echo.

echo ====================================
pause
