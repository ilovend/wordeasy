"""
词库分割工具 - 将大词库分割为小块便于上传
使用方法: python split_vocabulary.py input.txt 500
"""
import sys
import os

def split_vocabulary(input_file, chunk_size=500):
    """
    将词库文件分割为多个小文件
    参数:
    - input_file: 输入文件路径
    - chunk_size: 每个文件的单词数（默认500）
    """
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(os.path.dirname(input_file), f"{base_name}_parts")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total = len(lines)
    num_parts = (total + chunk_size - 1) // chunk_size
    
    print(f"=" * 60)
    print(f"词库分割工具")
    print(f"=" * 60)
    print(f"输入文件: {input_file}")
    print(f"总单词数: {total}")
    print(f"分割大小: {chunk_size} 词/文件")
    print(f"分割数量: {num_parts} 个文件")
    print(f"=" * 60)
    
    for i in range(num_parts):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, total)
        chunk = lines[start:end]
        
        output_file = os.path.join(output_dir, f"{base_name}_part{i+1:02d}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(chunk))
        
        print(f"✓ Part {i+1:2d}: {len(chunk):4d} 词 -> {os.path.basename(output_file)}")
    
    print(f"=" * 60)
    print(f"分割完成！")
    print(f"输出目录: {output_dir}")
    print(f"=" * 60)
    print(f"\n上传建议:")
    print(f"1. 在WordEasy中依次上传 part01, part02, part03...")
    print(f"2. 每个文件约 {chunk_size} 词，上传速度更快")
    print(f"3. 系统会自动去重，放心上传")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python split_vocabulary.py <词库文件> [每份单词数]")
        print("示例: python split_vocabulary.py cet4.txt 500")
        sys.exit(1)
    
    input_file = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 {input_file}")
        sys.exit(1)
    
    split_vocabulary(input_file, chunk_size)
