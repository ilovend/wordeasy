# 🚀 快速开始指南

## 5分钟快速启动 WordEasy

### 📋 前置要求

- Python 3.8+
- Node.js 16+
- Git

### ⚡ 一键安装（推荐）

#### 1️⃣ 克隆项目
```bash
git clone https://github.com/ilovend/wordeasy.git
cd wordeasy
```

#### 2️⃣ 运行安装脚本
```bash
# 自动检测环境、安装依赖、初始化数据库
python setup.py
```

#### 3️⃣ 启动项目

**Windows:**
```bash
# 双击运行或命令行执行
restart.bat
```

**macOS/Linux:**
```bash
# 添加执行权限并运行
chmod +x start.sh
./start.sh
```

#### 4️⃣ 访问应用
在浏览器打开: **http://localhost:5173** 🎉

---

## 🔧 手动安装（可选）

### 步骤1: 安装后端

```bash
cd backend

# 创建数据目录
mkdir data

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py
```

### 步骤2: 安装前端

```bash
cd frontend

# 安装依赖
npm install
```

### 步骤3: 启动服务

```bash
# 终端1 - 启动后端
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2 - 启动前端
cd frontend
npm run dev
```

---

## 🐛 常见问题快速修复

### ❌ 端口被占用
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### ❌ Python模块未找到
```bash
cd backend
pip install -r requirements.txt
```

### ❌ 数据库文件错误
```bash
cd backend
# 删除旧数据库
rm -rf data/wordeasy.db  # Linux/macOS
del data\wordeasy.db     # Windows

# 重新初始化
python init_db.py
```

### ❌ npm安装失败
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 下一步

- 📖 阅读完整文档: [README.md](README.md)
- 🔧 详细安装说明: [INSTALL.md](INSTALL.md)
- 🤝 参与贡献: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🌐 在线演示: [Demo](https://your-demo-link.com)

---

## 💬 需要帮助？

- 📝 查看 [Issues](https://github.com/ilovend/wordeasy/issues)
- 💬 参与 [Discussions](https://github.com/ilovend/wordeasy/discussions)
- 📧 联系作者: ilovendme@outlook.com

---

**祝你使用愉快！** 如果觉得有帮助，请给个 ⭐️ Star！
