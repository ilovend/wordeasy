# WordEasy 后端启动脚本
# 使用方法：cd backend; .\start_backend.ps1

Write-Host "🚀 启动 WordEasy 后端服务..." -ForegroundColor Green

# 检查是否已安装依赖
if (-not (Test-Path "venv")) {
    Write-Host "📦 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
Write-Host "🔧 激活虚拟环境..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# 安装依赖
Write-Host "📥 安装依赖包..." -ForegroundColor Cyan
pip install -r requirements.txt

# 检查数据库是否存在
if (-not (Test-Path "data\wordeasy.db")) {
    Write-Host "🗄️ 初始化数据库..." -ForegroundColor Yellow
    python init_db.py
}

# 启动服务
Write-Host "`n✅ 启动FastAPI服务..." -ForegroundColor Green
Write-Host "API地址: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Yellow
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
