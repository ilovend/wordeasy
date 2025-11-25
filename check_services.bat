@echo off
chcp 65001 > nul
echo ====================================
echo WordEasy 服务诊断
echo ====================================
echo.

echo [检查端口占用]
echo 8000端口（后端）:
netstat -ano | findstr ":8000"
echo.
echo 5173端口（前端）:
netstat -ano | findstr ":5173"
echo.

echo [测试后端API]
curl -s http://localhost:8000/api/progress
echo.
echo.

echo [后端进程]
tasklist | findstr python.exe
echo.

echo [前端进程]
tasklist | findstr node.exe
echo.

echo ====================================
pause
