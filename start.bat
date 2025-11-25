@echo off
chcp 65001 >nul
title WordEasy 启动器

echo.
echo ========================================
echo   WordEasy - 拼写攻防战
echo ========================================
echo.

cd /d "%~dp0"

echo [启动中] 正在启动后端服务...
start "WordEasy-后端" cmd /k "cd backend && start.bat"

echo [等待] 等待后端启动...
timeout /t 3 /nobreak >nul

echo [启动中] 正在启动前端服务...
start "WordEasy-前端" cmd /k "cd frontend && start.bat"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo   前端应用: http://localhost:5173
echo.
echo   两个服务窗口已打开
echo   请等待几秒让服务完全启动
echo   然后访问: http://localhost:5173
echo.
echo ========================================
echo.

pause
