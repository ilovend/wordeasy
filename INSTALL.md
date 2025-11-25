# 安装指南

本文档提供 WordEasy 项目的详细安装步骤。

## 📋 系统要求

### 必需软件
- **Python** 3.8 或更高版本
- **Node.js** 16.x 或更高版本
- **npm** 或 **yarn** 包管理器
- **Git** (用于克隆仓库)

### 推荐环境
- 操作系统: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- 内存: 4GB RAM 或更多
- 磁盘空间: 至少 500MB 可用空间

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/wordeasy.git
cd wordeasy
```

### 2. 安装后端

#### 2.1 创建虚拟环境（推荐）

**Windows:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 安装Python依赖

```bash
pip install -r requirements.txt
```

#### 2.3 初始化数据库

数据库会在第一次运行时自动创建。你也可以手动初始化：

```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

### 3. 安装前端

```bash
cd frontend
npm install
# 或使用 yarn
yarn install
```

### 4. 配置环境变量（可选）

#### 后端配置

创建 `backend/.env` 文件：

```env
DATABASE_URL=sqlite:///./data/wordeasy.db
CORS_ORIGINS=http://localhost:5173
```

#### 前端配置

创建 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=/api
```

## 🎯 运行项目

### 方式1: 使用启动脚本（Windows）

```powershell
.\restart.bat
```

这会自动启动后端和前端服务。

### 方式2: 手动启动

#### 启动后端

```bash
cd backend
# 确保虚拟环境已激活
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 http://localhost:8000 运行

#### 启动前端（新终端窗口）

```bash
cd frontend
npm run dev
```

前端将在 http://localhost:5173 运行

## ✅ 验证安装

### 检查后端

访问 http://localhost:8000/docs 查看API文档

或使用curl测试：
```bash
curl http://localhost:8000/
```

应该返回：
```json
{"message":"Welcome to WordEasy API","version":"1.0.0"}
```

### 检查前端

在浏览器中打开 http://localhost:5173

你应该看到 WordEasy 主页。

## 🐛 常见问题

### 问题1: Python模块未找到

**错误**: `ModuleNotFoundError: No module named 'fastapi'`

**解决方案**:
```bash
pip install -r requirements.txt
```

### 问题2: 端口被占用

**错误**: `Address already in use`

**解决方案**:

Windows:
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000
# 终止进程
taskkill /PID <进程ID> /F
```

macOS/Linux:
```bash
# 查找并终止占用端口的进程
lsof -ti:8000 | xargs kill -9
```

### 问题3: npm安装失败

**错误**: `npm ERR! code EACCES`

**解决方案**:
```bash
# 清除npm缓存
npm cache clean --force
# 删除node_modules
rm -rf node_modules package-lock.json
# 重新安装
npm install
```

### 问题4: 数据库权限错误

**错误**: `PermissionError: [Errno 13] Permission denied`

**解决方案**:
```bash
# 确保data目录存在且有写权限
mkdir -p backend/data
chmod 755 backend/data
```

### 问题5: 虚拟环境激活失败 (Windows PowerShell)

**错误**: `无法加载文件 xxx.ps1，因为在此系统上禁止运行脚本`

**解决方案**:
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔧 高级配置

### 修改端口

#### 后端端口
编辑启动命令或配置文件：
```bash
uvicorn app.main:app --port 8080
```

#### 前端端口
编辑 `frontend/vite.config.js`:
```javascript
export default {
  server: {
    port: 3000
  }
}
```

### 生产环境部署

参考 [部署文档](DEPLOYMENT.md)（待创建）

## 📚 下一步

- 阅读 [README.md](README_GITHUB.md) 了解项目功能
- 查看 [贡献指南](CONTRIBUTING.md) 参与开发
- 访问 [API文档](http://localhost:8000/docs)

## 💬 获取帮助

如果遇到问题：

1. 查看 [FAQ](docs/FAQ.md)
2. 搜索 [Issues](https://github.com/yourusername/wordeasy/issues)
3. 创建新的 [Issue](https://github.com/yourusername/wordeasy/issues/new)
4. 加入 [Discussions](https://github.com/yourusername/wordeasy/discussions)

---

祝你使用愉快！🎉
