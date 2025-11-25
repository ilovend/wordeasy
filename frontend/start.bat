@echo off
chcp 65001 >nul
title WordEasy 前端服务

echo.
echo ========================================
echo   WordEasy 前端服务启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查依赖...
if not exist "node_modules" (
    echo 正在安装npm依赖，请稍候...
    call npm install
    if errorlevel 1 (
        echo npm安装失败！
        pause
        exit /b 1
    )
) else (
    echo 依赖已安装 ✓
)

echo.
echo [2/2] 启动Vite开发服务器...
echo.
echo ========================================
echo   前端应用: http://localhost:5173
echo ========================================
echo.

call npm run dev

pause
