"""
CSV词库转换为WordEasy格式
使用方法：python convert_csv.py input.csv output.txt
"""
import csv
import sys

def convert_csv_to_wordeasy(input_file, output_file):
    """
    将CSV格式的词库转换为WordEasy格式
    CSV格式：word,meaning 或 word,meaning,其他列
    输出格式：word|meaning
    """
    count = 0
    skipped = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            with open(output_file, 'w', encoding='utf-8') as out:
                for row in reader:
                    # 跳过空行或列数不足的行
                    if len(row) < 2:
                        skipped += 1
                        continue
                    
                    word = row[0].strip().lower()
                    meaning = row[1].strip()
                    
                    # 跳过空白内容
                    if not word or not meaning:
                        skipped += 1
                        continue
                    
                    # 写入格式：word|meaning
                    out.write(f"{word}|{meaning}\n")
                    count += 1
        
        print(f"✓ 转换完成！")
        print(f"  成功转换: {count} 个单词")
        print(f"  跳过: {skipped} 行")
        print(f"  输出文件: {output_file}")
        
    except FileNotFoundError:
        print(f"✗ 错误：找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法：python convert_csv.py <输入CSV文件> <输出TXT文件>")
        print("示例：python convert_csv.py words.csv output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_csv_to_wordeasy(input_file, output_file)
