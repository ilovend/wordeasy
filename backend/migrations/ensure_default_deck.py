"""
快速修复：确保默认词库存在
适用于未运行完整迁移脚本的情况
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

def ensure_default_deck():
    """确保默认词库存在"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    print("检查默认词库...")
    
    with engine.connect() as conn:
        # 检查 decks 表是否存在
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='decks'
        """))
        
        if not result.fetchone():
            print("❌ decks 表不存在")
            print("请先运行完整迁移: python backend/migrations/add_deck_system.py")
            return False
        
        # 检查默认词库是否存在
        result = conn.execute(text("""
            SELECT COUNT(*) as count FROM decks WHERE id = 1
        """))
        
        if result.fetchone()[0] == 0:
            print("创建默认词库...")
            conn.execute(text("""
                INSERT INTO decks (
                    id, name, description, daily_new_limit, new_batch_size,
                    target_language, voice_type, deck_type, algorithm,
                    new_priority, review_priority, duplicate_filter,
                    total_words, learned_words, is_active
                ) VALUES (
                    1, '默认词库', '系统默认词库，包含所有导入的单词', 
                    100, 30, '英语', '默认', '单词库', 'FSRS',
                    '默认', '默认', '过滤', 0, 0, 1
                )
            """))
            conn.commit()
            print("✅ 默认词库创建成功")
        else:
            print("✅ 默认词库已存在")
        
        return True

if __name__ == "__main__":
    if ensure_default_deck():
        print("\n可以继续使用了！")
    else:
        print("\n需要运行完整迁移脚本")
        sys.exit(1)
