# convert_vocab.py 快速使用指南

## 🚀 基本使用

### 最简单的方式（推荐）

```bash
# 自动检测格式并转换
python convert_vocab.py input.csv output.txt
python convert_vocab.py words.json output.txt
```

工具会自动识别：
- ✅ CSV 格式 (`.csv`)
- ✅ JSON 格式 (`.json`)
- ✅ 文本格式 (`.txt`)
- ✅ ECDICT 数据库 (`.db`, `.sqlite`)

---

## 📚 支持的输入格式

### 1. CSV 格式
```csv
hello,你好
world,世界
study,学习；研究
```

### 2. JSON 格式（对象数组）
```json
[
  {"word": "book", "meaning": "书"},
  {"word": "read", "meaning": "阅读"}
]
```

### 3. JSON 格式（键值对）
```json
{
  "hello": "你好",
  "world": "世界"
}
```

### 4. 文本格式（空格/Tab分隔）
```
hello 你好
world 世界
study 学习；研究
```

### 5. ECDICT 数据库
```bash
python convert_vocab.py ecdict.db output.txt --limit 2000
```

---

## 🎯 常见场景

### 场景1：转换CSV词库
```bash
python convert_vocab.py cet4.csv cet4.txt
```

### 场景2：转换JSON词库
```bash
python convert_vocab.py vocabulary.json vocab.txt
```

### 场景3：从ECDICT提取高频词
```bash
# 提取3000个词频≥20的高频词
python convert_vocab.py ecdict.db high_freq.txt --limit 3000 --min-frq 20
```

### 场景4：手动指定格式
```bash
# 如果文件没有扩展名或扩展名不标准
python convert_vocab.py unknown.dat output.txt --format json
```

---

## 📤 输出格式

统一的 WordEasy 格式：
```
word|释义
```

示例：
```
hello|你好
world|世界
study|学习；研究
```

---

## ⚙️ 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `input` | 输入文件路径 | `words.csv` |
| `output` | 输出文件路径 | `output.txt` |
| `-f, --format` | 手动指定格式 | `--format json` |
| `-l, --limit` | ECDICT提取数量 | `--limit 5000` |
| `--min-frq` | ECDICT最小词频 | `--min-frq 15` |

---

## 💡 使用技巧

### 技巧1：批量转换
```bash
# Windows PowerShell
Get-ChildItem *.json | ForEach-Object {
    python convert_vocab.py $_.Name "$($_.BaseName).txt"
}

# Linux/Mac
for file in *.json; do
    python convert_vocab.py "$file" "${file%.json}.txt"
done
```

### 技巧2：查看转换结果
```bash
# Windows
python convert_vocab.py words.csv output.txt; Get-Content output.txt -Head 5

# Linux/Mac
python convert_vocab.py words.csv output.txt && head -5 output.txt
```

### 技巧3：ECDICT词频推荐
- `min-frq=5`：包含较多单词，适合初学者
- `min-frq=10`：常用词，默认推荐
- `min-frq=20`：高频词，适合快速掌握
- `min-frq=50`：核心词汇

---

## ❓ 常见问题

### Q1: 转换后中文乱码？
**A**: 确保输入文件是 UTF-8 编码。可用记事本"另存为"选择UTF-8编码。

### Q2: 提示"找不到文件"？
**A**: 检查文件路径是否正确，可使用绝对路径：
```bash
python convert_vocab.py C:\Downloads\words.csv C:\Output\output.txt
```

### Q3: 自动检测格式不准确？
**A**: 使用 `--format` 手动指定：
```bash
python convert_vocab.py file.dat output.txt --format csv
```

### Q4: 单词被跳过？
**A**: 检查输入文件是否：
- 每行格式正确（有单词和释义）
- 没有空白行
- 分隔符正确（CSV用逗号，TXT用空格/Tab）

---

## 🆚 与旧工具的区别

| 特性 | convert_vocab.py | 旧工具 |
|------|------------------|--------|
| 自动检测 | ✅ | ❌ |
| 统一接口 | ✅ | ❌ |
| 详细提示 | ✅ | 基础 |
| 命令行参数 | 完整 | 部分 |

---

## 🔗 相关资源

- **完整文档**: `README.md`
- **词库资源**: `VOCABULARY_RESOURCES.md`
- **ECDICT下载**: https://github.com/skywind3000/ECDICT

---

**需要帮助？** 运行 `python convert_vocab.py --help` 查看详细说明。
