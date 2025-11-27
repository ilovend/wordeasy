"""
数据库迁移脚本 - 添加词库分类管理功能

执行方式：
python backend/migrations/add_deck_system.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models_v2 import Deck, Word, Progress, DailyStats
import datetime

def migrate_database():
    """执行数据库迁移"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    print("=" * 60)
    print("开始数据库迁移：添加词库分类管理功能")
    print("=" * 60)
    
    with engine.connect() as conn:
        # 1. 创建 decks 表
        print("\n步骤 1/5: 创建 decks 表...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR UNIQUE NOT NULL,
                description VARCHAR,
                daily_new_limit INTEGER DEFAULT 100,
                new_batch_size INTEGER DEFAULT 30,
                target_language VARCHAR DEFAULT '英语',
                voice_type VARCHAR DEFAULT '默认',
                deck_type VARCHAR DEFAULT '单词库',
                algorithm VARCHAR DEFAULT 'FSRS',
                new_priority VARCHAR DEFAULT '默认',
                review_priority VARCHAR DEFAULT '默认',
                duplicate_filter VARCHAR DEFAULT '过滤',
                total_words INTEGER DEFAULT 0,
                learned_words INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATE DEFAULT CURRENT_DATE
            )
        """))
        conn.commit()
        print("✅ decks 表创建成功")
        
        # 2. 创建默认词库
        print("\n步骤 2/5: 创建默认词库...")
        result = conn.execute(text("SELECT COUNT(*) as count FROM decks WHERE name = '默认词库'"))
        if result.fetchone()[0] == 0:
            conn.execute(text("""
                INSERT INTO decks (
                    name, description, daily_new_limit, new_batch_size,
                    target_language, voice_type, deck_type, algorithm
                ) VALUES (
                    '默认词库', '系统默认词库，包含所有导入的单词', 100, 30,
                    '英语', '默认', '单词库', 'FSRS'
                )
            """))
            conn.commit()
            print("✅ 默认词库创建成功")
        else:
            print("ℹ️  默认词库已存在，跳过")
        
        # 3. 备份旧的 words 表
        print("\n步骤 3/5: 备份旧数据...")
        conn.execute(text("CREATE TABLE IF NOT EXISTS words_backup AS SELECT * FROM words"))
        conn.commit()
        print("✅ 数据备份完成")
        
        # 4. 修改 words 表结构
        print("\n步骤 4/5: 更新 words 表结构...")
        try:
            # 创建新的 words 表
            conn.execute(text("DROP TABLE IF EXISTS words_new"))
            conn.execute(text("""
                CREATE TABLE words_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word VARCHAR NOT NULL,
                    zh_definition VARCHAR NOT NULL,
                    difficulty INTEGER NOT NULL CHECK(difficulty BETWEEN 1 AND 3),
                    category VARCHAR,
                    audio_url VARCHAR,
                    deck_id INTEGER NOT NULL,
                    created_at DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY(deck_id) REFERENCES decks(id)
                )
            """))
            
            # 迁移数据（所有旧单词归入默认词库）
            conn.execute(text("""
                INSERT INTO words_new (id, word, zh_definition, difficulty, category, audio_url, deck_id, created_at)
                SELECT id, word, zh_definition, difficulty, category, audio_url, 1, CURRENT_DATE
                FROM words_backup
            """))
            
            # 替换表
            conn.execute(text("DROP TABLE words"))
            conn.execute(text("ALTER TABLE words_new RENAME TO words"))
            
            # 创建索引
            conn.execute(text("CREATE INDEX idx_words_word ON words(word)"))
            conn.execute(text("CREATE INDEX idx_words_deck_id ON words(deck_id)"))
            
            conn.commit()
            print("✅ words 表结构更新成功")
        except Exception as e:
            print(f"⚠️  words 表更新失败: {e}")
            print("尝试恢复备份...")
            conn.rollback()
        
        # 5. 创建 daily_stats 表
        print("\n步骤 5/5: 创建 daily_stats 表...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER NOT NULL,
                stat_date DATE DEFAULT CURRENT_DATE,
                new_learned INTEGER DEFAULT 0,
                reviewed INTEGER DEFAULT 0,
                correct_count INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                study_time INTEGER DEFAULT 0,
                FOREIGN KEY(deck_id) REFERENCES decks(id)
            )
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_daily_stats_deck ON daily_stats(deck_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(stat_date)"))
        conn.commit()
        print("✅ daily_stats 表创建成功")
        
        # 6. 更新词库统计
        print("\n步骤 6/6: 更新词库统计...")
        conn.execute(text("""
            UPDATE decks 
            SET total_words = (SELECT COUNT(*) FROM words WHERE deck_id = decks.id),
                learned_words = (SELECT COUNT(*) 
                                FROM words w 
                                LEFT JOIN progress p ON w.id = p.word_id 
                                WHERE w.deck_id = decks.id AND p.mastery_level > 0)
        """))
        conn.commit()
        print("✅ 统计数据更新完成")
    
    print("\n" + "=" * 60)
    print("✅ 数据库迁移完成！")
    print("=" * 60)
    print("\n提示：")
    print("1. 所有旧单词已自动归入'默认词库'")
    print("2. 原始数据已备份到 'words_backup' 表")
    print("3. 可以开始创建新的词库分类了")
    print("\n重启服务以使用新功能：")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")

if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        print("\n如需帮助，请查看错误日志")
        sys.exit(1)
