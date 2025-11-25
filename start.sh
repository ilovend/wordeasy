#!/bin/bash
# WordEasy 启动脚本 (Linux/macOS)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   Starting WordEasy Services...    ${NC}"
echo -e "${BLUE}=====================================${NC}"
echo

# 检查是否在项目根目录
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 停止已有进程
echo -e "${YELLOW}[1/4] 停止已有进程...${NC}"
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 2

# 检查数据目录
echo -e "${YELLOW}[2/4] 检查数据目录...${NC}"
if [ ! -d "backend/data" ]; then
    mkdir -p backend/data
    echo -e "${GREEN}✓ 已创建 backend/data 目录${NC}"
fi

# 检查数据库
if [ ! -f "backend/data/wordeasy.db" ]; then
    echo -e "${YELLOW}数据库不存在，正在初始化...${NC}"
    cd backend
    python3 init_db.py || python init_db.py
    cd ..
    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
else
    echo -e "${GREEN}✓ 数据库已存在${NC}"
fi

# 启动后端
echo -e "${YELLOW}[3/4] 启动后端服务...${NC}"
cd backend
if command -v python3 &> /dev/null; then
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
else
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
fi
BACKEND_PID=$!
cd ..
sleep 3
echo -e "${GREEN}✓ 后端服务已启动 (PID: $BACKEND_PID)${NC}"

# 启动前端
echo -e "${YELLOW}[4/4] 启动前端服务...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
sleep 2
echo -e "${GREEN}✓ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"

echo
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}   Services started successfully!   ${NC}"
echo -e "${BLUE}=====================================${NC}"
echo
echo -e "${BLUE}后端服务:${NC} http://localhost:8000"
echo -e "${BLUE}前端应用:${NC} http://localhost:5173"
echo -e "${BLUE}API文档:${NC}  http://localhost:8000/docs"
echo
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo

# 等待信号
trap "echo -e '\n${YELLOW}正在停止服务...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 保持脚本运行
wait
