"""
JSON词库转换为WordEasy格式
使用方法：python convert_json.py input.json output.txt
"""
import json
import sys

def convert_json_to_wordeasy(input_file, output_file):
    """
    将JSON格式的词库转换为WordEasy格式
    支持多种JSON结构：
    1. [{"word": "hello", "meaning": "你好"}, ...]
    2. {"hello": "你好", "world": "世界", ...}
    """
    count = 0
    skipped = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(output_file, 'w', encoding='utf-8') as out:
            # 处理列表格式
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # 尝试不同的键名
                        word = (item.get('word') or item.get('en') or 
                               item.get('english') or item.get('term', '')).strip().lower()
                        meaning = (item.get('meaning') or item.get('zh') or 
                                 item.get('chinese') or item.get('definition', '')).strip()
                        
                        if word and meaning:
                            out.write(f"{word}|{meaning}\n")
                            count += 1
                        else:
                            skipped += 1
            
            # 处理字典格式 {"word": "meaning"}
            elif isinstance(data, dict):
                for word, meaning in data.items():
                    word = word.strip().lower()
                    meaning = str(meaning).strip()
                    
                    if word and meaning:
                        out.write(f"{word}|{meaning}\n")
                        count += 1
                    else:
                        skipped += 1
        
        print(f"✓ 转换完成！")
        print(f"  成功转换: {count} 个单词")
        print(f"  跳过: {skipped} 条")
        print(f"  输出文件: {output_file}")
        
    except FileNotFoundError:
        print(f"✗ 错误：找不到文件 {input_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"✗ 错误：{input_file} 不是有效的JSON文件")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法：python convert_json.py <输入JSON文件> <输出TXT文件>")
        print("示例：python convert_json.py words.json output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_json_to_wordeasy(input_file, output_file)
