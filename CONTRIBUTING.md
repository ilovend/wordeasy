# 贡献指南

感谢您对 WordEasy 项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告Bug

如果你发现了bug，请：
1. 检查 [Issues](https://github.com/yourusername/wordeasy/issues) 确认该问题未被报告
2. 创建新Issue，包含以下信息：
   - Bug的详细描述
   - 复现步骤
   - 预期行为和实际行为
   - 环境信息（操作系统、浏览器版本等）
   - 截图或错误日志（如有）

### 提交功能建议

如果你有好的想法：
1. 在 [Issues](https://github.com/yourusername/wordeasy/issues) 中创建 Feature Request
2. 清晰描述功能的目的和价值
3. 如有可能，提供实现思路或参考案例

### 提交代码

#### 开发流程

1. **Fork 项目**
   ```bash
   # 在GitHub上点击Fork按钮
   git clone https://github.com/your-username/wordeasy.git
   cd wordeasy
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行开发**
   - 遵循项目代码规范
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # 或
   git commit -m "fix: resolve bug"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 在GitHub上创建PR
   - 填写PR模板
   - 等待代码审查

#### 提交信息规范

使用语义化提交信息：

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `perf:` 性能优化
- `test:` 测试相关
- `chore:` 构建/工具链相关

示例：
```
feat: 添加单词收藏功能
fix: 修复拼写检查时的空格问题
docs: 更新安装说明
```

## 📝 代码规范

### Python (后端)

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)：

```python
# 好的示例
def get_word_by_id(db: Session, word_id: int) -> Optional[Word]:
    """根据ID获取单词"""
    return db.query(Word).filter(Word.id == word_id).first()

# 避免
def getWord(db,id):
    return db.query(Word).filter(Word.id==id).first()
```

### JavaScript/Vue (前端)

遵循项目 ESLint 配置：

```javascript
// 好的示例
async function submitAnswer(userInput) {
  if (!userInput.trim()) return
  
  const result = await gameStore.submitAnswer(userInput)
  if (result.correct) {
    showSuccess()
  }
}

// 避免
async function submitAnswer(userInput){
    if(!userInput.trim())return;
    const result=await gameStore.submitAnswer(userInput);
    if(result.correct){showSuccess();}
}
```

### Vue 组件

```vue
<template>
  <!-- 简洁的模板 -->
  <div class="container">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup>
// Composition API
import { ref, computed } from 'vue'

const title = ref('WordEasy')
</script>

<style scoped>
/* 使用 Tailwind CSS 或 scoped 样式 */
</style>
```

## 🧪 测试

### 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

### 编写测试

确保新功能有对应的测试：

```python
# backend/tests/test_crud.py
def test_get_word_by_id(db_session):
    """测试通过ID获取单词"""
    word = create_test_word(db_session)
    result = crud.get_word_by_id(db_session, word.id)
    assert result.word == "test"
```

## 📚 文档

更新文档时请确保：

- 文档清晰易懂
- 包含代码示例
- 更新相关的README和注释
- 检查拼写和语法

## 🔍 代码审查

提交PR后：

1. 自动化检查（CI/CD）会运行
2. 维护者会审查代码
3. 根据反馈进行修改
4. 审查通过后合并

## ❓ 需要帮助？

- 📖 查看 [文档](README.md)
- 💬 在 [Discussions](https://github.com/yourusername/wordeasy/discussions) 提问
- 📧 发送邮件至 ilovendme@outlook.com

## 🎉 贡献者

感谢所有贡献者！

<!-- 这里会自动生成贡献者列表 -->

---

再次感谢你的贡献！ 🙏
