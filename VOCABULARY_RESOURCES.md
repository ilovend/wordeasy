# WordEasy 词库资源指南

本文档提供多种英语单词词库资源，帮助你扩展WordEasy的学习内容。所有词库均支持TXT格式，可直接导入使用。

---

## 📚 一、开源词库资源（推荐）

### 1. KyleBing/english-vocabulary ⭐推荐
**内容**：四六级（CET4/CET6）、考研、SAT等考试词汇，按难度分级  
**格式**：TXT、JSON  
**特点**：分类清晰，适合开发背单词应用  
**链接**：https://github.com/KyleBing/english-vocabulary

**使用方法**：
1. 下载对应的TXT文件（如：CET4.txt）
2. 转换格式为 `word|中文释义`（每行一个单词）
3. 在WordEasy词库管理页面上传

---

### 2. mahavivo/english-wordlists
**内容**：日常词汇、专业术语（计算机、医学等）  
**格式**：TXT、CSV  
**特点**：词库全面，支持按词频、场景筛选  
**链接**：https://github.com/mahavivo/english-wordlists

**适用场景**：
- 专业领域学习（IT、医学等）
- 按词频分级学习

---

### 3. skywind3000/ECDICT ⭐推荐
**内容**：77万+词条，涵盖雅思、托福、GRE  
**格式**：SQLite（可导出TXT）  
**特点**：包含音标、释义、例句  
**链接**：https://github.com/skywind3000/ECDICT

**优势**：
- 数据最全面
- 包含音标和例句
- 适合高级学习者

---

## 🛠️ 二、自定义生成工具

### 1. Vocabulary.com
**功能**：粘贴英文文本，自动筛选生词并生成词表  
**特点**：结合语境（原句），支持导出TXT  
**链接**：https://www.vocabulary.com/

**使用步骤**：
1. 粘贴英文文章/小说片段
2. 系统自动识别生词
3. 导出为TXT格式
4. 上传到WordEasy

---

### 2. 幕境（MuJing）
**功能**：从电影、美剧、文档生成词库  
**特点**：词库关联真实场景，支持字幕导入  
**链接**：https://github.com/tangshimin/MuJing

**适用场景**：
- 看剧学英语
- 电影爱好者
- 情景化学习

---

### 3. WordTower
**功能**：导入电子书、字幕，生成学习词本  
**特点**：自动区分生词/熟词  
**平台**：iOS App Store

---

## 💻 三、词库管理软件

### 1. 欧路词典
**功能**：支持导入MDD/MDX/TXT格式  
**特点**：多设备同步，单词本功能  
**链接**：https://www.eudic.net/

---

### 2. 灵格斯词典（Lingoes）
**功能**：支持TXT、CSV格式，自定义结构  
**特点**：轻量级，屏幕取词  
**链接**：http://www.lingoes.cn/

---

## 📝 四、WordEasy词库格式说明

### 标准格式
```
word|中文释义
```

### 示例
```
abandon|放弃
ability|能力
absent|缺席的
absorb|吸收
abstract|抽象的
```

### 格式要求
- ✅ UTF-8编码
- ✅ 每行一个单词
- ✅ 使用 `|` 分隔英文和中文
- ✅ 英文单词小写
- ❌ 不要有空行
- ❌ 不要有重复单词

---

## 🔄 五、格式转换指南

### 常见格式转换

#### 1. CSV转TXT
如果词库是CSV格式（如：`word,meaning`）：

**Excel/WPS方法**：
1. 打开CSV文件
2. 将逗号替换为 `|`（查找替换功能）
3. 另存为TXT格式（UTF-8编码）

**Python脚本**：
```python
# convert_csv_to_txt.py
import csv

with open('input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    with open('output.txt', 'w', encoding='utf-8') as out:
        for row in reader:
            if len(row) >= 2:
                out.write(f"{row[0]}|{row[1]}\n")
```

#### 2. JSON转TXT
如果词库是JSON格式：

```python
# convert_json_to_txt.py
import json

with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    with open('output.txt', 'w', encoding='utf-8') as out:
        for item in data:
            word = item.get('word', '')
            meaning = item.get('meaning', '')
            if word and meaning:
                out.write(f"{word}|{meaning}\n")
```

#### 3. SQLite转TXT（针对ECDICT）
```python
# convert_ecdict_to_txt.py
import sqlite3

conn = sqlite3.connect('ecdict.db')
cursor = conn.cursor()

# 查询前1000个常用词
cursor.execute("""
    SELECT word, translation 
    FROM stardict 
    WHERE frq > 0 
    ORDER BY frq DESC 
    LIMIT 1000
""")

with open('ecdict_output.txt', 'w', encoding='utf-8') as f:
    for word, translation in cursor.fetchall():
        # 只保留中文释义
        if translation:
            zh = translation.split('\\n')[0]  # 取第一行
            f.write(f"{word}|{zh}\n")

conn.close()
```

---

## 🎯 六、推荐词库组合

### 入门学习者
- **KyleBing/CET4** - 4000个四级词汇
- **日常高频词** - WordEasy内置100词

### 考试备考
- **CET6** - 六级词汇
- **考研词汇** - 5500词
- **雅思/托福** - ECDICT筛选

### 进阶学习者
- **GRE词汇** - ECDICT高级词
- **专业术语** - mahavivo专业词库
- **影视词汇** - 幕境生成

---

## ⚠️ 七、注意事项

### 1. 格式兼容性
- 确保TXT文件是UTF-8编码
- 使用正确的分隔符 `|`
- 避免特殊字符

### 2. 版权问题
- 开源词库遵守License（如MIT、GPL）
- 商业使用需查看授权
- 自定义词库注意版权合规

### 3. 词库质量
- ✅ 优先选择有例句、音标的词库
- ✅ 注意词义的准确性
- ✅ 定期更新词库

### 4. 导入建议
- 首次导入建议200-500词测试
- 避免一次导入过多（影响性能）
- 定期清理重复单词

---

## 🚀 八、快速开始

### 推荐流程
1. **下载词库**：从GitHub下载 KyleBing/CET4.txt
2. **格式转换**：转换为 `word|释义` 格式
3. **测试导入**：先导入50词测试
4. **批量导入**：确认格式无误后批量导入
5. **开始学习**：在WordEasy中开始拼写挑战

### 示例词库下载
我们在项目中提供了 `example_words.txt` 作为格式参考。

---

## 📞 九、获取帮助

如果在词库导入过程中遇到问题：

1. 检查文件编码（必须是UTF-8）
2. 检查格式（每行：`word|释义`）
3. 查看错误提示（在上传页面显示）
4. 使用示例文件 `example_words.txt` 作为参考

---

## 🔗 十、相关链接

### GitHub开源词库
- KyleBing/english-vocabulary: https://github.com/KyleBing/english-vocabulary
- mahavivo/english-wordlists: https://github.com/mahavivo/english-wordlists
- skywind3000/ECDICT: https://github.com/skywind3000/ECDICT

### 在线工具
- Vocabulary.com: https://www.vocabulary.com/
- 幕境MuJing: https://github.com/tangshimin/MuJing

### 词典软件
- 欧路词典: https://www.eudic.net/
- 灵格斯词典: http://www.lingoes.cn/

---

**开始扩展你的词库，让学习更高效！** 📚✨
