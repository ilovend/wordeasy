"""
ECDICT SQLite数据库词库提取工具
使用方法：python convert_ecdict.py ecdict.db output.txt [limit]
"""
import sqlite3
import sys

def extract_from_ecdict(db_file, output_file, limit=1000, min_frq=10):
    """
    从ECDICT数据库提取词库
    参数：
    - db_file: ECDICT数据库文件路径
    - output_file: 输出TXT文件路径
    - limit: 提取单词数量（默认1000）
    - min_frq: 最小词频（默认10，越大越常用）
    """
    count = 0
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 查询常用词（按词频排序）
        query = """
            SELECT word, translation 
            FROM stardict 
            WHERE frq >= ? 
            ORDER BY frq DESC 
            LIMIT ?
        """
        
        print(f"正在从数据库提取词汇...")
        cursor.execute(query, (min_frq, limit))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for word, translation in cursor.fetchall():
                if not translation:
                    continue
                
                # 提取中文释义（通常在第一行）
                lines = translation.split('\\n')
                zh_meaning = ""
                
                for line in lines:
                    # 跳过音标行
                    if line.startswith('[') or line.startswith('/'):
                        continue
                    # 查找包含中文的行
                    if any('\u4e00' <= c <= '\u9fff' for c in line):
                        # 清理格式（去除词性标记等）
                        zh_meaning = line.strip()
                        # 去除常见前缀
                        for prefix in ['n. ', 'v. ', 'adj. ', 'adv. ', 'prep. ', 'conj. ']:
                            if zh_meaning.startswith(prefix):
                                zh_meaning = zh_meaning[len(prefix):]
                        break
                
                if zh_meaning:
                    f.write(f"{word.lower()}|{zh_meaning}\n")
                    count += 1
        
        conn.close()
        
        print(f"✓ 提取完成！")
        print(f"  成功提取: {count} 个单词")
        print(f"  词频要求: >={min_frq}")
        print(f"  输出文件: {output_file}")
        
    except sqlite3.Error as e:
        print(f"✗ 数据库错误: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"✗ 错误：找不到文件 {db_file}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 提取失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法：python convert_ecdict.py <ECDICT数据库> <输出TXT文件> [数量]")
        print("示例：python convert_ecdict.py ecdict.db output.txt 2000")
        print("\n数据库下载：https://github.com/skywind3000/ECDICT")
        sys.exit(1)
    
    db_file = sys.argv[1]
    output_file = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    extract_from_ecdict(db_file, output_file, limit)
