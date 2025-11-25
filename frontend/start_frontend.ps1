# WordEasy 前端启动脚本
# 使用方法：cd frontend; .\start_frontend.ps1

Write-Host "🎨 启动 WordEasy 前端开发服务器..." -ForegroundColor Green

# 检查是否已安装依赖
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 安装npm依赖..." -ForegroundColor Yellow
    npm install
}

# 启动开发服务器
Write-Host "`n✅ 启动Vite开发服务器..." -ForegroundColor Green
Write-Host "应用地址: http://localhost:5173" -ForegroundColor Yellow
npm run dev
