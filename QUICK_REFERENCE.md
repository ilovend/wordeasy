# WordEasy 快速参考指南

## 🚀 5分钟快速上手

### 1. 启动应用
```powershell
# 在项目根目录
.\start.ps1
```

### 2. 访问应用
打开浏览器：http://localhost:5173

### 3. 开始游戏
首页 → 开始闯关 → 选择难度 → 输入拼写 → 提交

---

## 📖 常用命令

### 后端命令
```powershell
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务
python -m uvicorn app.main:app --reload

# 查看API文档
# 浏览器打开 http://localhost:8000/docs
```

### 前端命令
```powershell
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

---

## 🎮 游戏玩法

### 拼写攻防战
1. 选择难度（初级/中级/高级）
2. 看中文释义，输入英文拼写
3. 正确：+10分，消灭怪物
4. 错误：-1生命值
5. 完成10题或生命值归零则结束

### 难度说明
- **初级**：3-5字母，常用词（如：cat, dog, apple）
- **中级**：6-8字母，考试词（如：analyze, benefit）
- **高级**：长单词，易混词（如：environment, intelligence）

---

## 📚 功能导航

### 首页 `/`
- 查看学习进度（等级、金币、掌握度）
- 快速入口：开始闯关、复习模式、词库管理

### 游戏页 `/game`
- 拼写攻防战主游戏

### 复习页 `/review`
- 今日复习：基于遗忘曲线推送
- 错词歼灭战：专攻历史错误单词
- 速拼挑战：60秒10词

### 词库页 `/library`
- 上传自定义词库（TXT格式）
- 查看词库统计
- 错词本列表
- 待复习单词列表

---

## 📝 自定义词库格式

### TXT文件格式
```
单词|中文释义
```

### 示例（每行一个单词）
```
abandon|放弃
ability|能力
absent|缺席的
```

### 上传步骤
1. 准备TXT文件（UTF-8编码）
2. 进入词库管理页面
3. 点击上传按钮
4. 选择文件并上传
5. 查看导入结果

---

## 🔧 常见问题

### Q: 后端启动失败？
A: 检查端口8000是否被占用，或修改端口
```powershell
python -m uvicorn app.main:app --port 8001
```

### Q: 前端启动失败？
A: 检查Node版本（需要16+），重新安装依赖
```powershell
rm -r node_modules
npm install
```

### Q: 数据库文件在哪？
A: `backend/data/wordeasy.db`

### Q: 如何重置数据库？
A: 删除数据库文件后重新初始化
```powershell
rm backend/data/wordeasy.db
python backend/init_db.py
```

### Q: 如何修改内置单词？
A: 编辑 `backend/init_db.py` 的 `INITIAL_WORDS` 列表

---

## 🎯 学习建议

### 每日计划
1. **早上**：复习昨日错词（10分钟）
2. **中午**：新单词挑战（15分钟）
3. **晚上**：今日复习推送（10分钟）

### 进阶技巧
- 专注掌握一个难度后再升级
- 重视错词本，重复练习
- 利用自定义词库针对性学习
- 每周查看进度，调整策略

### 效率提升
- 🔴 陌生词：每天3次密集复习
- 🟡 熟悉词：隔天复习巩固
- 🟢 掌握词：每周抽查保持

---

## 📊 API接口速查

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/words` | GET | 获取单词（?difficulty=1&limit=10） |
| `/api/words/review` | GET | 待复习单词 |
| `/api/words/errors` | GET | 错词本 |
| `/api/spell/check` | POST | 检查拼写 |
| `/api/progress` | GET | 学习进度 |
| `/api/words/upload` | POST | 上传词库 |

完整文档：http://localhost:8000/docs

---

## 🔄 数据流程

### 拼写检查流程
```
用户输入 → submitAnswer() 
→ api.checkSpelling() 
→ POST /api/spell/check 
→ 后端验证 + update_progress() 
→ 返回结果 + 下次复习时间 
→ 前端显示反馈
```

### 复习推送流程
```
每日启动 → fetchProgress() 
→ GET /api/words/review 
→ 后端查询 next_review <= today 
→ 返回待复习单词 
→ 前端展示列表
```

---

## 🎨 自定义样式

### 修改主题色
编辑 `frontend/tailwind.config.js`：
```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',  // 修改主色调
      success: '#10B981',
      danger: '#EF4444',
    }
  }
}
```

### 修改字体
编辑 `frontend/src/style.css`：
```css
body {
  font-family: 'Your Font', sans-serif;
}
```

---

## 📦 项目文件速查

| 文件 | 用途 |
|------|------|
| `start.ps1` | 一键启动 |
| `backend/init_db.py` | 初始化数据库 |
| `backend/app/main.py` | API端点定义 |
| `backend/app/crud.py` | 复习算法实现 |
| `frontend/src/components/SpellGame.vue` | 游戏主组件 |
| `frontend/src/stores/game.js` | 游戏状态管理 |
| `example_words.txt` | 词库示例 |

---

## 🚀 生产部署

### 后端部署
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### 前端部署
```bash
# 构建静态文件
npm run build

# dist目录包含所有静态文件
# 可部署到任意静态托管服务
```

---

## 🔗 相关文档

- [完整需求文档](README.md)
- [使用说明](PROJECT_README.md)
- [项目结构](STRUCTURE.md)
- [开发总结](COMPLETION_SUMMARY.md)

---

**快速参考完毕！开始你的单词学习之旅吧！** 🎉
