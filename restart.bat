@echo off
chcp 65001 > nul
echo ====================================
echo 正在重启 WordEasy 服务...
echo ====================================

echo.
echo [1/3] 停止现有进程...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Frontend*" 2>nul
timeout /t 2 /nobreak > nul

echo [2/3] 清理端口...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173"') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak > nul

echo [3/3] 启动服务...
cd /d "%~dp0"
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak > nul
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo ✓ 服务重启完成！
echo.
echo 后端: http://localhost:8000
echo 前端: http://localhost:5173
echo API文档: http://localhost:8000/docs
echo.
echo 请刷新浏览器页面（Ctrl+F5）
echo ====================================
pause
