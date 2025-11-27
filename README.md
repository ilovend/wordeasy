# 🎮 WordEasy - 拼写攻防战

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Vue](https://img.shields.io/badge/vue-3.3.8-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Setup Automated](https://img.shields.io/badge/setup-automated-success.svg)

**一个基于科学记忆法的交互式英语单词拼写学习工具**

[📖 快速开始](QUICKSTART.md) | [🎯 功能特性](#-功能特性) | [💡 使用指南](#-使用指南) | [❓ 常见问题](docs/FAQ.md) | [🤝 贡献指南](CONTRIBUTING.md)

<img src="docs/screenshot.png" alt="WordEasy Screenshot" width="800"/>

</div>

---

## 📖 项目简介

WordEasy 是一个轻量级的英语单词学习应用，通过游戏化的方式帮助用户掌握单词拼写。项目采用前后端分离架构，结合艾宾浩斯遗忘曲线算法，提供智能的复习提醒系统。

### 🎯 核心特点

- 🎮 **游戏化学习** - 拼写攻防战，让学习充满趣味
- 📚 **三种模式** - 学习模式、挑战模式、复习模式，循序渐进
- 🧠 **智能复习** - 基于遗忘曲线的科学复习算法（1天→3天→15天）
- 🎵 **语音朗读** - 集成Web Speech API，支持单词发音
- 📊 **学习统计** - 实时追踪学习进度和掌握程度
- 💾 **本地存储** - SQLite数据库，无需云端服务器
- 🎨 **精美UI** - Tailwind CSS打造的现代化界面
- 📱 **响应式设计** - 支持桌面端和移动端

---

## ✨ 功能特性

### 🎓 学习模式
- 浏览单词，查看释义
- 自动播放发音（2次重复）
- 键盘快捷键支持（←→/AD 切换，Space 标记，R 复读）
- 学习进度条实时显示

### ⚔️ 挑战模式
- 限时拼写测试（90秒）
- 生命值系统（3条命）
- 积分奖励机制
- 拼写错误实时对比显示
- **必须答对才能继续**（答错需重新拼写）

### 🔄 复习模式
- 今日待复习单词提醒
- **错词本模式**：专门练习历史错误单词
- 基于掌握程度的智能推送
- 遗忘曲线算法优化（1天→3天→7天→15天）

### 🎯 用户体验增强
- **Toast通知系统**：优雅的消息提示
- **加载状态反馈**：LoadingSpinner组件
- **友好的错误提示**：统一的错误处理

### 📚 词库管理
- 内置400+分级单词
- **多格式支持**：TXT、CSV、JSON 自动识别
- **三种导入方式**：
  - ✏️ 快速添加：手动输入单个单词
  - 📋 批量添加：粘贴多行文本（支持空格/Tab/竖线分隔）
  - 📤 文件导入：上传词库文件（100+单词）
- **在线格式转换器**：CSV/JSON → WordEasy标准格式
- 智能难度分类（基于单词长度和词缀）
- 词库统计和清空功能
- 详细指南：[词库导入完整指南](docs/WORD_IMPORT_GUIDE.md)

### 🎯 难度分级
- **初级** (1级): 3-5字母短单词，适合入门
- **中级** (2级): 6-9字母标准词汇
- **高级** (3级): 10+字母或高级词缀单词

---

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架（Composition API）
- **Pinia** - 轻量级状态管理
- **Tailwind CSS** - 实用优先的CSS框架
- **Axios** - HTTP客户端
- **Web Speech API** - 浏览器原生语音合成
- **Vite优化** - 代码分割、压缩配置
- **Toast组件** - 统一的消息通知系统
- **Loading组件** - 加载状态反馈

### 后端
- **FastAPI** - 现代化Python Web框架
- **SQLAlchemy** - Python ORM
- **SQLite** - 轻量级数据库
- **Pydantic** - 数据验证
- **缓存系统** - 内存缓存优化性能
- **性能监控** - API调用性能追踪

### 开发工具
- **Vite** - 前端构建工具
- **Uvicorn** - ASGI服务器
- **PowerShell** - 自动化脚本

---

## 🚀 快速开始

> **⚡ 3步快速启动，5分钟开始使用！**

### 环境要求

- **Python** 3.8+
- **Node.js** 16+
- **npm** 或 **yarn**

### 🎯 一键安装（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/ilovend/wordeasy.git
cd wordeasy

# 2. 运行安装脚本（自动检测环境、安装依赖、初始化数据库）
python setup.py

# 3. 启动项目
# Windows 用户:
restart.bat

# macOS/Linux 用户:
chmod +x start.sh
./start.sh

# 4. 在浏览器打开: http://localhost:5173
```

### 📝 手动安装

<details>
<summary>点击展开查看详细步骤</summary>

**1. 克隆项目**
```bash
git clone https://github.com/ilovend/wordeasy.git
cd wordeasy
```

**2. 后端安装**
```bash
cd backend

# 创建数据目录（会自动创建，但可以手动创建）
mkdir data

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（可选，首次启动会自动创建）
python init_db.py
```

**3. 前端安装**
```bash
cd frontend
npm install
# 或使用 yarn
yarn install
```

**4. 启动应用**

```bash
# 终端1 - 启动后端（端口8000）
cd backend
python -m uvicorn app.main:app --reload

# 终端2 - 启动前端（端口5173）
cd frontend
npm run dev
```

访问应用：**http://localhost:5173**

</details>

### 🆘 遇到问题？

查看 [快速开始指南](QUICKSTART.md) 或 [安装文档](INSTALL.md)

---

## 🚀 快速开始

### 环境要求

- **Python** 3.8+
- **Node.js** 16+
- **npm** 或 **yarn**

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/wordeasy.git
cd wordeasy
```

2. **后端安装**
```bash
cd backend
pip install -r requirements.txt
```

3. **前端安装**
```bash
cd frontend
npm install
# 或使用 yarn
yarn install
```

### 启动应用

#### 方式1：使用启动脚本（推荐）
```powershell
# Windows PowerShell
.\restart.bat

# 或使用 PowerShell 脚本
.\start.ps1
```

#### 方式2：分别启动
```bash
# 终端1 - 启动后端（端口8000）
cd backend
python -m uvicorn app.main:app --reload

# 终端2 - 启动前端（端口5173）
cd frontend
npm run dev
```

访问应用：**http://localhost:5173**

---

## 📂 项目结构

```
wordeasy/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI主应用
│   │   ├── models.py       # 数据库模型
│   │   ├── schemas.py      # Pydantic模型
│   │   ├── crud.py         # 数据库操作
│   │   ├── cache.py        # 🆕 缓存系统
│   │   ├── performance.py  # 🆕 性能监控
│   │   ├── word_classifier.py  # 智能分类算法
│   │   └── database.py     # 数据库连接
│   ├── migrations/         # 🆕 数据库迁移脚本
│   ├── data/
│   │   └── wordeasy.db     # SQLite数据库
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   │   ├── SpellGame.vue      # 主游戏组件
│   │   │   ├── WordManager.vue    # 词库管理
│   │   │   ├── LoadingSpinner.vue # 🆕 加载组件
│   │   │   └── Settings.vue       # 设置页面
│   │   ├── stores/         # Pinia状态管理
│   │   │   ├── game.js     # 游戏状态（含错词本模式）
│   │   │   └── settings.js # 设置状态
│   │   ├── api/            # API封装（含错误处理）
│   │   ├── utils/          # 工具函数
│   │   │   └── toast.js    # 🆕 Toast通知系统
│   │   └── router/         # 路由配置
│   └── package.json        # 前端依赖
├── tools/                  # 工具脚本
│   └── generate_words.py   # 词库生成器
├── restart.bat             # 一键启动脚本
└── README.md               # 项目文档
```

---

## 🎮 使用指南

### 学习流程

1. **选择难度** - 在主页选择初级/中级/高级
2. **学习模式** - 浏览单词，标记已学习的单词
3. **开始挑战** - 全部学完后进入限时拼写测试
4. **查看结果** - 测试结束后查看成绩和错误统计
5. **复习巩固** - 第二天系统会提醒复习

### 快捷键

#### 学习模式
- `←` / `A` - 上一个单词
- `→` / `D` - 下一个单词
- `Space` - 标记为已学习
- `R` - 复读发音
- `Enter` - 开始挑战
- `ESC` - 退出

#### 挑战模式
- `Enter` - 提交答案
- `ESC` - 退出挑战

### 自定义词库

创建TXT文件，每行格式：`单词|中文释义`

示例：
```
abandon|放弃
benefit|好处
challenge|挑战
```

在词库管理页面上传即可。

---

## 📊 数据库设计

### Words 表（单词）
```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    zh_definition TEXT NOT NULL,
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 3),
    category TEXT,
    audio_url TEXT
);
```

### Progress 表（学习进度）
```sql
CREATE TABLE progress (
    word_id INTEGER PRIMARY KEY,
    mastery_level INTEGER DEFAULT 0,  -- 0陌生/1熟悉/2掌握
    next_review DATE,                 -- 下次复习日期 (索引)
    error_count INTEGER DEFAULT 0,    -- 错误次数 (索引)
    last_reviewed DATE,               -- 🆕 最后复习日期
    review_count INTEGER DEFAULT 0,   -- 🆕 复习次数
    FOREIGN KEY (word_id) REFERENCES words(id)
);

-- 性能优化索引
CREATE INDEX ix_progress_next_review ON progress(next_review);
CREATE INDEX ix_progress_error_count ON progress(error_count);
```

---

## 🔧 配置说明

### 后端配置
在 `backend/app/database.py` 中修改数据库路径：
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/wordeasy.db"
```

### 前端配置
在 `frontend/src/api/index.js` 中修改API地址：
```javascript
const API_BASE_URL = '/api'  // 开发环境
// const API_BASE_URL = 'http://your-server.com/api'  // 生产环境
```

在 `vite.config.js` 中配置代理：
```javascript
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

---

## 🧪 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm run test
```

---

## 📦 部署

### 生产构建

**前端打包**：
```bash
cd frontend
npm run build
```

**后端部署**：
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker部署（可选）
```bash
docker-compose up -d
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

### 代码规范
- Python: 遵循 PEP 8
- JavaScript: 遵循 ESLint 配置
- 提交信息: 使用语义化提交规范

---

## 📝 更新日志

### v1.3.0 (2025-01-26) 🎉
- ✨ **错词本模式**：专门练习历史错误单词
- 🎨 **Toast通知系统**：优雅的消息提示（4种类型）
- ⚡ **LoadingSpinner组件**：改善加载状态反馈
- 📊 **性能监控工具**：API调用性能追踪
- 🚀 **Vite构建优化**：代码分割和压缩配置
- 💾 **后端缓存系统**：SimpleCache类和@cached装饰器
- 🔍 **数据库索引优化**：next_review和error_count字段索引
- 📈 **新增Progress字段**：last_reviewed和review_count
- 🔧 **CI/CD修复**：升级GitHub Actions到v4/v5版本
- 🎯 **错误处理增强**：统一的友好错误消息

### v1.2.0 (2025-01-25)
- ✨ 新增复习模式和今日复习提醒
- ✨ 添加学习记录系统（基于遗忘曲线）
- 🐛 修复挑战模式答错后无法输入的问题
- 🎨 优化UI动画和交互体验
- 🔊 改进语音播放逻辑

### v1.1.0 (2025-01-20)
- ✨ 新增学习模式
- ✨ 添加键盘快捷键支持
- ✨ 实现智能难度分类
- 🎨 重构UI界面

### v1.0.0 (2025-01-15)
- 🎉 首次发布
- ✨ 基础拼写游戏功能
- ✨ 词库管理功能

[查看完整更新日志](CHANGELOG.md)

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👥 作者

- **Your Name** - *Initial work* - [YourGithub](https://github.com/yourusername)

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) - 浏览器语音功能

---

## 📮 联系方式

- 项目主页: [https://github.com/yourusername/wordeasy](https://github.com/yourusername/wordeasy)
- Issue追踪: [https://github.com/yourusername/wordeasy/issues](https://github.com/yourusername/wordeasy/issues)
- 邮箱: ilovendme@outlook.com

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by [ilovend](https://github.com/ilovend)

</div>
