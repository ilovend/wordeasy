# 词库格式转换工具

这个文件夹包含多个Python脚本，用于将不同格式的词库转换为WordEasy支持的格式。

## 📋 工具列表

### 1. convert_csv.py - CSV转换工具
将CSV格式的词库转换为WordEasy格式。

**使用方法**：
```bash
python convert_csv.py input.csv output.txt
```

**支持的CSV格式**：
- `word,meaning`
- `word,meaning,其他列`

**示例**：
```bash
python convert_csv.py cet4.csv cet4_wordeasy.txt
```

---

### 2. convert_json.py - JSON转换工具
将JSON格式的词库转换为WordEasy格式。

**使用方法**：
```bash
python convert_json.py input.json output.txt
```

**支持的JSON格式**：
```json
// 格式1：对象数组
[
  {"word": "hello", "meaning": "你好"},
  {"word": "world", "meaning": "世界"}
]

// 格式2：键值对
{
  "hello": "你好",
  "world": "世界"
}
```

**示例**：
```bash
python convert_json.py words.json words_wordeasy.txt
```

---

### 3. convert_ecdict.py - ECDICT数据库提取工具
从ECDICT SQLite数据库提取常用词汇。

**使用方法**：
```bash
python convert_ecdict.py ecdict.db output.txt [数量]
```

**参数说明**：
- `ecdict.db`: ECDICT数据库文件（从GitHub下载）
- `output.txt`: 输出文件名
- `数量`: 提取单词数量（可选，默认1000）

**示例**：
```bash
# 提取1000个最常用词
python convert_ecdict.py ecdict.db common_words.txt

# 提取5000个常用词
python convert_ecdict.py ecdict.db common_5k.txt 5000
```

**ECDICT下载地址**：https://github.com/skywind3000/ECDICT

---

## 🎯 输出格式

所有工具的输出格式统一为：
```
word|中文释义
```

每行一个单词，使用 `|` 分隔英文和中文。

---

## 💡 使用建议

1. **先测试小文件**：转换前先用小文件测试，确保格式正确
2. **检查编码**：确保输入文件是UTF-8编码
3. **去重处理**：如需要，可在WordEasy中上传时自动去重
4. **分批导入**：建议每次导入200-500词，避免一次性导入过多

---

## 🔧 环境要求

Python 3.6+ （无需额外依赖，使用标准库）

---

## 📝 示例工作流

### 从GitHub下载词库并转换

```bash
# 1. 克隆词库仓库
git clone https://github.com/KyleBing/english-vocabulary.git

# 2. 进入工具目录
cd wordeasy/tools

# 3. 转换词库（假设是CSV格式）
python convert_csv.py ../../english-vocabulary/CET4.csv cet4.txt

# 4. 上传到WordEasy
# 在浏览器中打开 http://localhost:5173
# 进入词库管理 → 上传 cet4.txt
```

---

## ⚠️ 注意事项

1. **路径问题**：使用相对路径或绝对路径
2. **文件编码**：输入文件必须是UTF-8编码
3. **格式验证**：转换后检查输出文件前几行
4. **版权合规**：使用开源词库注意License

---

## 🚀 快速开始

```bash
# 测试CSV转换
python convert_csv.py ../example_words.txt test.txt

# 查看结果
cat test.txt
```

---

**需要帮助？** 查看主文档：[VOCABULARY_RESOURCES.md](../VOCABULARY_RESOURCES.md)
