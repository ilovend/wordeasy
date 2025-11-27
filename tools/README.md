# 词库格式转换工具

这个文件夹包含智能词库转换工具，用于将不同格式的词库转换为WordEasy支持的格式。

## 🚀 快速开始

**推荐使用统一工具**：
```bash
python convert_vocab.py <输入文件> <输出文件> [选项]
```

`convert_vocab.py` 可以**自动识别**文件格式并转换，支持 CSV、JSON、TXT、ECDICT 数据库。

---

## 📋 convert_vocab.py - 智能转换工具（推荐）

### 基本用法

```bash
# 自动检测格式并转换
python convert_vocab.py words.csv output.txt
python convert_vocab.py words.json output.txt
python convert_vocab.py vocab.txt output.txt
python convert_vocab.py ecdict.db output.txt
```

### 高级选项

```bash
# 手动指定格式
python convert_vocab.py unknown.dat output.txt --format json

# ECDICT数据库选项
python convert_vocab.py ecdict.db output.txt --limit 2000 --min-frq 15

# 查看帮助
python convert_vocab.py --help
```

### 支持的格式

| 格式 | 扩展名 | 示例格式 |
|------|--------|----------|
| **CSV** | `.csv` | `word,meaning` 或 `word,meaning,其他列` |
| **JSON** | `.json` | `[{"word":"hello","meaning":"你好"}]` 或 `{"hello":"你好"}` |
| **TXT** | `.txt` | `word 释义` 或 `word	释义` （空格或Tab分隔）|
| **ECDICT** | `.db`, `.sqlite` | ECDICT SQLite数据库 |

### JSON格式详解

支持多种JSON结构：

```json
// 格式1：对象数组
[
  {"word": "hello", "meaning": "你好"},
  {"en": "world", "zh": "世界"}
]

// 格式2：键值对
{
  "hello": "你好",
  "world": "世界"
}
```

支持的键名：
- 单词：`word`, `en`, `english`, `term`, `vocab`
- 释义：`meaning`, `zh`, `chinese`, `definition`, `translation`

### ECDICT数据库

```bash
# 提取1000个最常用词（默认）
python convert_vocab.py ecdict.db output.txt

# 提取5000个高频词（词频≥15）
python convert_vocab.py ecdict.db output.txt --limit 5000 --min-frq 15
```

**参数说明**：
- `--limit`: 提取单词数量
- `--min-frq`: 最小词频（越大越常用，默认10）

**ECDICT下载**：https://github.com/skywind3000/ECDICT

---

## 📚 传统转换工具（向后兼容）

如果你更喜欢使用单独的工具，以下脚本仍然可用：

### convert_csv.py
```bash
python convert_csv.py input.csv output.txt
```

### convert_json.py
```bash
python convert_json.py input.json output.txt
```

### convert_ecdict.py
```bash
python convert_ecdict.py ecdict.db output.txt [数量]
```

### convert_kylebing.py
批量转换KyleBing词库的专用脚本。

---

## 🎯 输出格式

所有工具的输出格式统一为：
```
word|中文释义
```

每行一个单词，使用 `|` 分隔英文和中文。

示例：
```
hello|你好
world|世界
study|学习；研究
```

---

## 💡 使用建议

1. **优先使用 convert_vocab.py**：自动检测格式，减少出错
2. **先测试小文件**：转换前先用小文件测试，确保格式正确
3. **检查编码**：确保输入文件是UTF-8编码
4. **分批导入**：建议每次导入200-500词，避免一次性导入过多

---

## 🔧 环境要求

Python 3.6+ （无需额外依赖，使用标准库）

---

## 📝 示例工作流

### 场景1：转换在线下载的CSV词库

```bash
# 1. 下载词库（例如从GitHub）
# 2. 进入工具目录
cd wordeasy/tools

# 3. 一键转换
python convert_vocab.py ~/Downloads/cet4.csv cet4.txt

# 4. 查看结果
head cet4.txt
```

### 场景2：从ECDICT提取高频词

```bash
# 1. 下载ECDICT数据库
# 从 https://github.com/skywind3000/ECDICT 下载 ecdict.db

# 2. 提取3000个最常用词
python convert_vocab.py ecdict.db high_freq_3k.txt --limit 3000 --min-frq 20

# 3. 上传到WordEasy
# 在浏览器中打开 http://localhost:5173
# 进入词库管理 → 上传 high_freq_3k.txt
```

### 场景3：批量转换多个文件

```bash
# 使用shell循环批量转换
for file in *.json; do
    python convert_vocab.py "$file" "${file%.json}.txt"
done
```

---

## 🔍 自动格式检测规则

`convert_vocab.py` 使用以下规则自动检测格式：

1. **扩展名检测**：
   - `.csv` → CSV格式
   - `.json` → JSON格式
   - `.db`, `.sqlite`, `.sqlite3` → ECDICT数据库
   - `.txt` → 文本格式

2. **内容检测**（无扩展名时）：
   - 以 `{` 或 `[` 开头 → JSON格式
   - 包含逗号且不包含 `|` → CSV格式
   - 其他 → 文本格式

3. **手动指定**（推荐处理未知格式）：
   ```bash
   python convert_vocab.py unknown.dat output.txt --format json
   ```

---

## ⚠️ 注意事项

1. **文件编码**：输入文件必须是UTF-8编码
2. **格式验证**：转换后检查输出文件前几行
3. **版权合规**：使用开源词库注意License
4. **数据质量**：ECDICT词频越高的词越常用，建议 min-frq ≥ 10

---

## 🆚 工具对比

| 特性 | convert_vocab.py | 单独工具 |
|------|------------------|----------|
| 自动检测格式 | ✅ | ❌ |
| 命令行参数 | ✅ | 部分 |
| 错误提示 | 详细 | 基础 |
| 使用难度 | 简单 | 中等 |
| 维护状态 | 主推 | 兼容 |

---

**需要帮助？** 查看主文档：[VOCABULARY_RESOURCES.md](../VOCABULARY_RESOURCES.md)
