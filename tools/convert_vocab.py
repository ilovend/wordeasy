"""
WordEasy 词库智能转换工具
自动识别输入格式并转换为 WordEasy 标准格式

支持格式：
- CSV: word,meaning 或 word,meaning,其他列
- JSON: 数组格式或对象格式
- TXT: word [空格/Tab] meaning
- SQLite: ECDICT 数据库

使用方法：
  python convert_vocab.py <输入文件> <输出文件> [选项]

示例：
  python convert_vocab.py words.csv output.txt
  python convert_vocab.py words.json output.txt
  python convert_vocab.py ecdict.db output.txt --limit 2000
  python convert_vocab.py vocab.txt output.txt
"""

import sys
import os
import csv
import json
import sqlite3
import re
import argparse
from pathlib import Path


class VocabConverter:
    """词库转换器基类"""
    
    def __init__(self, input_file, output_file, **options):
        self.input_file = input_file
        self.output_file = output_file
        self.options = options
        self.count = 0
        self.skipped = 0
    
    def convert(self):
        """执行转换（需子类实现）"""
        raise NotImplementedError
    
    def write_word(self, out_file, word, meaning):
        """写入标准格式"""
        word = word.strip().lower()
        meaning = meaning.strip()
        
        if word and meaning:
            out_file.write(f"{word}|{meaning}\n")
            self.count += 1
            return True
        else:
            self.skipped += 1
            return False
    
    def print_result(self):
        """打印转换结果"""
        print(f"\n✓ 转换完成！")
        print(f"  成功转换: {self.count} 个单词")
        if self.skipped > 0:
            print(f"  跳过: {self.skipped} 条")
        print(f"  输出文件: {self.output_file}")


class CSVConverter(VocabConverter):
    """CSV格式转换器"""
    
    def convert(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                with open(self.output_file, 'w', encoding='utf-8') as out:
                    for row in reader:
                        if len(row) >= 2:
                            self.write_word(out, row[0], row[1])
                        else:
                            self.skipped += 1
            
            self.print_result()
            return True
            
        except Exception as e:
            print(f"✗ CSV转换失败: {e}")
            return False


class JSONConverter(VocabConverter):
    """JSON格式转换器"""
    
    def convert(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(self.output_file, 'w', encoding='utf-8') as out:
                if isinstance(data, list):
                    # 数组格式: [{"word": "hello", "meaning": "你好"}, ...]
                    for item in data:
                        if isinstance(item, dict):
                            word = self._extract_word(item)
                            meaning = self._extract_meaning(item)
                            if word and meaning:
                                self.write_word(out, word, meaning)
                            else:
                                self.skipped += 1
                
                elif isinstance(data, dict):
                    # 对象格式: {"hello": "你好", "world": "世界"}
                    for word, meaning in data.items():
                        self.write_word(out, word, str(meaning))
            
            self.print_result()
            return True
            
        except json.JSONDecodeError:
            print(f"✗ 错误：{self.input_file} 不是有效的JSON文件")
            return False
        except Exception as e:
            print(f"✗ JSON转换失败: {e}")
            return False
    
    def _extract_word(self, item):
        """从字典中提取单词"""
        for key in ['word', 'en', 'english', 'term', 'vocab']:
            if key in item:
                return str(item[key])
        return ''
    
    def _extract_meaning(self, item):
        """从字典中提取释义"""
        for key in ['meaning', 'zh', 'chinese', 'definition', 'translation']:
            if key in item:
                return str(item[key])
        return ''


class TXTConverter(VocabConverter):
    """文本格式转换器（支持空格或Tab分隔）"""
    
    def convert(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                with open(self.output_file, 'w', encoding='utf-8') as out:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # 尝试用|分隔（已经是标准格式）
                        if '|' in line:
                            parts = line.split('|', 1)
                            if len(parts) == 2:
                                self.write_word(out, parts[0], parts[1])
                                continue
                        
                        # 尝试用空格/Tab分隔
                        parts = re.split(r'\s+', line, maxsplit=1)
                        if len(parts) >= 2:
                            word = parts[0]
                            meaning = parts[1]
                            
                            # 清理释义（去除词性标记如 n. v. adj.）
                            meaning = re.sub(r'^[a-z]+\.\s*', '', meaning)
                            
                            self.write_word(out, word, meaning)
                        else:
                            self.skipped += 1
            
            self.print_result()
            return True
            
        except Exception as e:
            print(f"✗ TXT转换失败: {e}")
            return False


class ECDICTConverter(VocabConverter):
    """ECDICT数据库转换器"""
    
    def convert(self):
        limit = self.options.get('limit', 1000)
        min_frq = self.options.get('min_frq', 10)
        
        try:
            conn = sqlite3.connect(self.input_file)
            cursor = conn.cursor()
            
            # 检查表结构
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'stardict' not in tables:
                print(f"✗ 错误：数据库中没有找到 stardict 表")
                print(f"  可用表: {', '.join(tables)}")
                return False
            
            # 查询常用词
            query = """
                SELECT word, translation 
                FROM stardict 
                WHERE frq >= ? 
                ORDER BY frq DESC 
                LIMIT ?
            """
            
            print(f"正在从数据库提取词汇（词频>={min_frq}）...")
            cursor.execute(query, (min_frq, limit))
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for word, translation in cursor.fetchall():
                    if not translation:
                        self.skipped += 1
                        continue
                    
                    # 提取中文释义
                    zh_meaning = self._extract_chinese(translation)
                    
                    if zh_meaning:
                        self.write_word(f, word, zh_meaning)
                    else:
                        self.skipped += 1
            
            conn.close()
            
            print(f"  词频要求: >={min_frq}")
            self.print_result()
            return True
            
        except sqlite3.Error as e:
            print(f"✗ 数据库错误: {e}")
            return False
        except Exception as e:
            print(f"✗ ECDICT转换失败: {e}")
            return False
    
    def _extract_chinese(self, translation):
        """从translation字段提取中文释义"""
        lines = translation.split('\\n')
        
        for line in lines:
            # 跳过音标行
            if line.startswith('[') or line.startswith('/'):
                continue
            
            # 查找包含中文的行
            if any('\u4e00' <= c <= '\u9fff' for c in line):
                zh_meaning = line.strip()
                
                # 去除词性标记
                for prefix in ['n. ', 'v. ', 'adj. ', 'adv. ', 'prep. ', 'conj. ', 'pron. ']:
                    if zh_meaning.startswith(prefix):
                        zh_meaning = zh_meaning[len(prefix):]
                
                return zh_meaning
        
        return ""


def detect_format(file_path):
    """自动检测文件格式"""
    ext = Path(file_path).suffix.lower()
    
    # 根据扩展名判断
    if ext == '.csv':
        return 'csv'
    elif ext == '.json':
        return 'json'
    elif ext in ['.db', '.sqlite', '.sqlite3']:
        return 'ecdict'
    elif ext in ['.txt', '.text']:
        return 'txt'
    
    # 无扩展名时尝试读取内容判断
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            
            # JSON格式判断
            if first_line.startswith('{') or first_line.startswith('['):
                return 'json'
            
            # CSV格式判断（包含逗号且不包含|）
            if ',' in first_line and '|' not in first_line:
                return 'csv'
            
            # 默认文本格式
            return 'txt'
    
    except:
        return 'txt'


def main():
    parser = argparse.ArgumentParser(
        description='WordEasy 词库智能转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  python convert_vocab.py words.csv output.txt
  python convert_vocab.py words.json output.txt
  python convert_vocab.py vocab.txt output.txt
  python convert_vocab.py ecdict.db output.txt --limit 2000 --min-frq 15
  python convert_vocab.py unknown.dat output.txt --format json

支持的格式：
  csv    - CSV格式（word,meaning）
  json   - JSON格式（数组或对象）
  txt    - 文本格式（word [空格/Tab] meaning）
  ecdict - ECDICT SQLite数据库
        """
    )
    
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('-f', '--format', 
                       choices=['csv', 'json', 'txt', 'ecdict'],
                       help='手动指定输入格式（不指定则自动检测）')
    parser.add_argument('-l', '--limit', type=int, default=1000,
                       help='ECDICT: 提取单词数量（默认1000）')
    parser.add_argument('--min-frq', type=int, default=10,
                       help='ECDICT: 最小词频（默认10，越大越常用）')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"✗ 错误：找不到文件 {args.input}")
        return 1
    
    # 检测或使用指定格式
    file_format = args.format or detect_format(args.input)
    
    print("=" * 60)
    print(f"WordEasy 词库转换工具")
    print("=" * 60)
    print(f"输入文件: {args.input}")
    print(f"输出文件: {args.output}")
    print(f"检测格式: {file_format.upper()}")
    print("=" * 60)
    
    # 选择转换器
    converters = {
        'csv': CSVConverter,
        'json': JSONConverter,
        'txt': TXTConverter,
        'ecdict': ECDICTConverter,
    }
    
    converter_class = converters.get(file_format)
    if not converter_class:
        print(f"✗ 不支持的格式: {file_format}")
        return 1
    
    # 执行转换
    converter = converter_class(
        args.input, 
        args.output,
        limit=args.limit,
        min_frq=args.min_frq
    )
    
    success = converter.convert()
    
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
