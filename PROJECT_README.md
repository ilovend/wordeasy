# WordEasy - 拼写攻防战 🎮

一个基于Vue 3 + FastAPI的英语单词拼写学习游戏，通过游戏化的方式和科学的遗忘曲线算法，帮助用户轻松掌握英语拼写。

## 📖 文档导航

- 📘 [使用说明](PROJECT_README.md) - 本文档
- 📋 [需求文档](README.md) - 原始需求和设计文档
- 🏗️ [项目结构](STRUCTURE.md) - 详细的代码结构说明
- 📚 [词库资源](VOCABULARY_RESOURCES.md) - 词库下载和转换指南
- 🎯 [快速参考](QUICK_REFERENCE.md) - 常用命令速查
- ✅ [开发总结](COMPLETION_SUMMARY.md) - 项目完成情况

---

## ✨ 核心特性

- 🎯 **拼写攻防战**：三个难度等级，10个单词闯关模式
- 🧠 **智能复习算法**：基于遗忘曲线，自动生成复习计划
- 📚 **本地词库管理**：内置300词 + 支持自定义TXT导入
- 💾 **SQLite本地存储**：无需云端，所有数据本地保存
- 🎨 **精美UI设计**：Tailwind CSS响应式界面

## 📋 技术栈

### 后端
- **FastAPI** - 轻量级Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **SQLite** - 本地数据库存储
- **Uvicorn** - ASGI服务器

### 前端
- **Vue 3** - Composition API
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Tailwind CSS** - UI样式
- **Axios** - HTTP请求
- **Vite** - 构建工具

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 2. 后端安装与启动

```powershell
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库（创建表并导入300词）
python init_db.py

# 启动FastAPI服务（默认端口8000）
python -m uvicorn app.main:app --reload
```

后端API将运行在：`http://localhost:8000`
API文档：`http://localhost:8000/docs`

### 3. 前端安装与启动

```powershell
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器（默认端口5173）
npm run dev
```

前端应用将运行在：`http://localhost:5173`

## 📁 项目结构

```
wordeasy/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI主应用
│   │   ├── database.py     # 数据库配置
│   │   ├── models.py       # SQLAlchemy模型
│   │   ├── schemas.py      # Pydantic模式
│   │   └── crud.py         # 数据库操作
│   ├── data/
│   │   └── wordeasy.db     # SQLite数据库（运行后生成）
│   ├── init_db.py          # 数据库初始化脚本
│   └── requirements.txt    # Python依赖
│
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API请求封装
│   │   ├── components/    # Vue组件
│   │   │   ├── SpellGame.vue      # 拼写游戏组件
│   │   │   └── WordList.vue       # 词库管理组件
│   │   ├── stores/        # Pinia状态管理
│   │   │   ├── game.js
│   │   │   └── progress.js
│   │   ├── views/         # 页面视图
│   │   │   ├── Home.vue
│   │   │   ├── Game.vue
│   │   │   ├── WordLibrary.vue
│   │   │   └── Review.vue
│   │   ├── router/        # 路由配置
│   │   ├── App.vue        # 根组件
│   │   ├── main.js        # 入口文件
│   │   └── style.css      # 全局样式
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md              # 项目文档
```

## 📚 词库资源

WordEasy内置300个单词，你还可以：
- 📥 **导入更多词库** - 查看 [词库资源指南](VOCABULARY_RESOURCES.md)
- 🛠️ **格式转换工具** - 使用 `tools/` 目录下的转换脚本
- 🌐 **开源词库** - GitHub上有大量免费词库（四六级、考研、雅思等）

**推荐词库**：
- [KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary) - 四六级、考研词汇
- [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) - 77万词条，含音标例句

详见：[VOCABULARY_RESOURCES.md](VOCABULARY_RESOURCES.md)

---

## 🎮 功能说明

### 1. 拼写攻防战
- 选择难度（初级/中级/高级）
- 10个单词闯关，90秒限时
- 3点生命值，错误扣1点
- 正确+10积分，实时反馈

### 2. 智能复习算法
- **陌生词**（🔴）：当天复习3次
- **熟悉词**（🟡）：次日复习，间隔3/7/15天
- **掌握词**（🟢）：每周抽查
- 自动生成今日待复习列表

### 3. 词库管理
- 内置300词（日常100 + 考试100 + 兴趣100）
- 支持TXT文件导入（格式：`word|中文释义`）
- 词库统计：按难度和分类分组
- 错词本：历史错误单词重点复习

## 📊 API接口

### 单词相关
- `GET /api/words?difficulty=1&limit=10` - 获取指定难度单词
- `GET /api/words/review?limit=20` - 获取待复习单词
- `GET /api/words/errors?limit=20` - 获取错词本
- `POST /api/words/upload` - 上传自定义词库

### 拼写相关
- `POST /api/spell/check` - 检查拼写正确性

### 进度相关
- `GET /api/progress` - 获取学习进度统计

详细API文档见：`http://localhost:8000/docs`

## 🗃️ 数据库设计

### words表（单词表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| word | TEXT | 英文单词 |
| zh_definition | TEXT | 中文释义 |
| difficulty | INTEGER | 难度(1-3) |
| category | TEXT | 分类 |
| audio_url | TEXT | 发音URL（可选） |

### progress表（学习进度）
| 字段 | 类型 | 说明 |
|------|------|------|
| word_id | INTEGER | 外键(words.id) |
| mastery_level | INTEGER | 掌握度(0-2) |
| next_review | DATE | 下次复习日期 |
| error_count | INTEGER | 错误次数 |

## 🛠️ 开发计划

- [x] 基础拼写游戏功能
- [x] 智能复习算法
- [x] 词库管理
- [x] 错词本功能
- [ ] 发音功能（TTS集成）
- [ ] 速拼挑战模式优化
- [ ] 数据导出功能
- [ ] Electron打包为桌面应用

## 📝 使用示例

### 上传自定义词库

创建TXT文件（如`my_words.txt`）：
```
abandon|放弃
ability|能力
absent|缺席的
```

在"词库管理"页面上传该文件即可导入。

### 游戏流程

1. 首页查看学习进度
2. 点击"开始闯关"
3. 选择难度（初级/中级/高级）
4. 看到中文释义，输入英文拼写
5. 提交答案，查看反馈
6. 完成10个单词或生命值耗尽
7. 查看统计结果

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

WordEasy Team

---

**开始你的拼写冒险之旅吧！🚀**
