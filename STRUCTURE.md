# WordEasy 项目结构说明

## 📁 完整目录结构

```
wordeasy/
│
├── README.md                    # 需求文档
├── PROJECT_README.md            # 使用说明文档
├── .gitignore                   # Git忽略文件
├── start.ps1                    # 一键启动脚本
│
├── backend/                     # 后端目录
│   ├── app/                     # 应用包
│   │   ├── __init__.py         # 包初始化文件
│   │   ├── main.py             # FastAPI主应用，定义所有API端点
│   │   ├── database.py         # 数据库连接配置
│   │   ├── models.py           # SQLAlchemy数据模型（Word、Progress表）
│   │   ├── schemas.py          # Pydantic模式（API输入输出验证）
│   │   └── crud.py             # 数据库CRUD操作函数
│   │
│   ├── data/                    # 数据存储目录
│   │   └── wordeasy.db         # SQLite数据库（运行后自动生成）
│   │
│   ├── init_db.py              # 数据库初始化脚本（含300词）
│   ├── requirements.txt        # Python依赖列表
│   └── start_backend.ps1       # 后端启动脚本
│
├── frontend/                    # 前端目录
│   ├── public/                  # 静态资源
│   │
│   ├── src/                     # 源代码
│   │   ├── api/                 # API请求封装
│   │   │   └── index.js        # Axios封装，所有API调用
│   │   │
│   │   ├── components/          # 可复用组件
│   │   │   ├── SpellGame.vue   # 拼写游戏核心组件
│   │   │   └── WordList.vue    # 词库管理组件
│   │   │
│   │   ├── stores/              # Pinia状态管理
│   │   │   ├── game.js         # 游戏状态（单词、分数、生命值等）
│   │   │   └── progress.js     # 用户进度状态
│   │   │
│   │   ├── views/               # 页面视图
│   │   │   ├── Home.vue        # 首页（进度展示+功能入口）
│   │   │   ├── Game.vue        # 游戏页面
│   │   │   ├── WordLibrary.vue # 词库管理页面
│   │   │   └── Review.vue      # 复习模式页面
│   │   │
│   │   ├── router/              # 路由配置
│   │   │   └── index.js        # Vue Router配置
│   │   │
│   │   ├── App.vue             # 根组件
│   │   ├── main.js             # 入口文件（挂载Vue、Pinia、Router）
│   │   └── style.css           # 全局样式（Tailwind CSS）
│   │
│   ├── index.html              # HTML入口
│   ├── package.json            # npm配置和依赖
│   ├── vite.config.js          # Vite构建配置
│   ├── tailwind.config.js      # Tailwind CSS配置
│   ├── postcss.config.js       # PostCSS配置
│   └── start_frontend.ps1      # 前端启动脚本
```

## 📝 核心文件说明

### 后端核心文件

#### `backend/app/main.py`
FastAPI主应用，定义了所有API端点：
- `GET /api/words` - 获取指定难度单词
- `GET /api/words/review` - 获取待复习单词
- `GET /api/words/errors` - 获取错词本
- `POST /api/spell/check` - 检查拼写
- `GET /api/progress` - 获取学习进度
- `POST /api/words/upload` - 上传词库

#### `backend/app/models.py`
数据库模型定义：
- `Word` - 单词表（id, word, zh_definition, difficulty, category, audio_url）
- `Progress` - 学习进度表（word_id, mastery_level, next_review, error_count）

#### `backend/app/crud.py`
数据库操作函数，包含遗忘曲线算法实现：
- `update_progress()` - 根据正误更新掌握度和复习时间
- `get_review_words()` - 获取待复习单词
- `get_error_words()` - 获取错词

#### `backend/init_db.py`
数据库初始化脚本：
- 创建数据表
- 插入300个内置单词（日常100+考试100+兴趣100）
- 按难度和分类分组

### 前端核心文件

#### `frontend/src/components/SpellGame.vue`
拼写游戏核心组件：
- 难度选择界面
- 游戏进行界面（单词展示、输入、反馈）
- 游戏结束界面（统计结果）
- 计时器、生命值、积分系统

#### `frontend/src/components/WordList.vue`
词库管理组件：
- 上传自定义词库（TXT文件）
- 词库统计（按难度分类）
- 错词本列表
- 待复习单词列表

#### `frontend/src/stores/game.js`
游戏状态管理（Pinia）：
- 游戏状态（开始、进行、结束）
- 当前单词、分数、生命值
- 提交答案、切换单词、计时等方法

#### `frontend/src/api/index.js`
API请求封装（Axios）：
- 封装所有后端API调用
- 请求/响应拦截器
- 错误处理

## 🔄 数据流程

### 1. 游戏流程
```
用户选择难度 → 前端调用 getWords(difficulty) 
→ 后端返回10个单词 → 存储到 gameStore 
→ 用户输入拼写 → 调用 checkSpelling(wordId, input) 
→ 后端验证+更新进度 → 返回结果 
→ 前端展示反馈 → 继续下一题或结束
```

### 2. 复习算法流程
```
用户拼写单词 → 后端 crud.update_progress() 
→ 判断正误 → 调整 mastery_level 
→ 计算 next_review 日期（基于遗忘曲线）
→ 保存到 progress 表 
→ 前端下次可通过 getReviewWords() 获取待复习列表
```

### 3. 词库导入流程
```
用户上传TXT → 前端 uploadWords(file) 
→ 后端解析文件（每行：word|中文）
→ 去重+格式校验 → 批量插入 words 表 
→ 返回成功数量 → 前端显示结果
```

## 🛠️ 技术要点

### 后端技术要点
1. **FastAPI异步支持** - 高性能API服务
2. **SQLAlchemy ORM** - 类型安全的数据库操作
3. **Pydantic验证** - 自动API输入输出验证
4. **CORS中间件** - 允许前端跨域请求
5. **文件上传处理** - 支持multipart/form-data

### 前端技术要点
1. **Composition API** - Vue 3现代化开发方式
2. **Pinia状态管理** - 轻量级、类型安全
3. **Vue Router** - 单页面应用路由
4. **Tailwind CSS** - 实用优先的样式框架
5. **Vite** - 快速的构建工具

## 📊 数据库设计

### words表（单词表）
```sql
CREATE TABLE words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word TEXT NOT NULL UNIQUE,
  zh_definition TEXT NOT NULL,
  difficulty TINYINT CHECK(difficulty BETWEEN 1 AND 3),
  category TEXT,
  audio_url TEXT
);
```

### progress表（学习进度）
```sql
CREATE TABLE progress (
  word_id INTEGER PRIMARY KEY REFERENCES words(id),
  mastery_level TINYINT DEFAULT 0,  -- 0陌生/1熟悉/2掌握
  next_review DATE,
  error_count INTEGER DEFAULT 0
);
```

## 🎨 UI设计特点

1. **渐变背景** - 每个页面使用不同色调的渐变
2. **卡片设计** - 白色卡片+圆角+阴影
3. **响应式布局** - Grid布局适配移动端
4. **动画效果** - hover悬停、按钮点击动画
5. **状态反馈** - 正确/错误的颜色提示

## 🔧 开发建议

### 后端开发
1. 使用 `uvicorn --reload` 开启热重载
2. 访问 `/docs` 查看Swagger文档
3. 修改 `crud.py` 调整复习算法
4. 修改 `init_db.py` 更新内置词库

### 前端开发
1. 使用 `npm run dev` 开启热重载
2. 修改 `tailwind.config.js` 自定义主题
3. 在 `stores/` 添加新的状态管理
4. 在 `views/` 添加新页面

## 🚀 部署建议

### 本地部署
- 使用提供的 `.ps1` 启动脚本
- 数据存储在 `backend/data/wordeasy.db`

### 生产部署
1. **后端**：使用 Gunicorn + Uvicorn workers
2. **前端**：`npm run build` 生成静态文件
3. **数据库**：SQLite适合小型应用，大规模可迁移到PostgreSQL
4. **桌面应用**：可使用Electron打包

## 📚 扩展方向

1. **发音功能** - 集成TTS API（如Azure TTS）
2. **统计图表** - 添加学习曲线可视化
3. **社交功能** - 排行榜、分享成绩
4. **移动端** - 响应式优化或打包为原生应用
5. **多语言** - 支持其他外语学习

---

**开发完成！开始你的拼写冒险吧！** 🎉
