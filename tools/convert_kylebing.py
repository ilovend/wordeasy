"""
批量转换KyleBing词库为WordEasy格式
"""
import re
import os

def convert_kylebing_vocab(input_file, output_file):
    """转换格式: word [空格/制表符] 释义 -> word|释义"""
    count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        with open(output_file, 'w', encoding='utf-8') as out:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 使用正则分割（支持多个空格或制表符）
                parts = re.split(r'\s+', line, maxsplit=1)
                if len(parts) >= 2:
                    word = parts[0].strip().lower()
                    meaning = parts[1].strip()
                    
                    # 清理释义（去除词性标记）
                    meaning = re.sub(r'^[a-z]+\.\s*', '', meaning)
                    
                    if word and meaning:
                        out.write(f"{word}|{meaning}\n")
                        count += 1
    
    return count

# 批量转换词库
vocab_files = [
    ("1 初中-乱序.txt", "junior_high.txt", "初中"),
    ("2 高中-乱序.txt", "senior_high.txt", "高中"),
    ("3 四级-乱序.txt", "cet4.txt", "四级"),
    ("4 六级-乱序.txt", "cet6.txt", "六级"),
    ("5 考研-乱序.txt", "kaoyan.txt", "考研"),
    ("6 托福-乱序.txt", "toefl.txt", "托福"),
    ("7 SAT-乱序.txt", "sat.txt", "SAT"),
]

base_path = r"E:\ilovendProject\english-vocabulary"
output_path = r"E:\ilovendProject\wordeasy\vocabulary"

# 创建输出目录
os.makedirs(output_path, exist_ok=True)

print("=" * 50)
print("批量转换KyleBing词库")
print("=" * 50)

total = 0
for input_name, output_name, label in vocab_files:
    input_file = os.path.join(base_path, input_name)
    output_file = os.path.join(output_path, output_name)
    
    if os.path.exists(input_file):
        count = convert_kylebing_vocab(input_file, output_file)
        total += count
        print(f"✓ {label:6s} - {count:5d} 个单词 -> {output_name}")
    else:
        print(f"✗ {label:6s} - 文件不存在")

print("=" * 50)
print(f"转换完成！共 {total} 个单词")
print(f"输出目录: {output_path}")
print("=" * 50)
