@echo off
chcp 65001 >nul
title WordEasy 后端服务

echo.
echo ========================================
echo   WordEasy 后端服务启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查数据库...
if not exist "data\wordeasy.db" (
    echo 数据库不存在，正在初始化...
    python init_db.py
    if errorlevel 1 (
        echo 数据库初始化失败！
        pause
        exit /b 1
    )
) else (
    echo 数据库已存在 ✓
)

echo.
echo [2/3] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
)
echo 依赖检查完成 ✓

echo.
echo [3/3] 启动FastAPI服务...
echo.
echo ========================================
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo ========================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
