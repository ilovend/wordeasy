"""
数据库迁移脚本：添加性能索引
添加 next_review 和 error_count 索引以优化查询性能
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import SessionLocal, engine
from app.models import Base, Progress
from sqlalchemy import inspect, Index, text

def check_index_exists(inspector, table_name, index_name):
    """检查索引是否存在"""
    indexes = inspector.get_indexes(table_name)
    return any(idx['name'] == index_name for idx in indexes)

def add_performance_indexes():
    """添加性能索引"""
    print("开始添加性能索引...")
    
    inspector = inspect(engine)
    
    # 检查 progress 表是否存在
    if 'progress' not in inspector.get_table_names():
        print("警告: progress 表不存在，跳过迁移")
        return
    
    # 添加 next_review 索引
    if not check_index_exists(inspector, 'progress', 'ix_progress_next_review'):
        print("添加 next_review 索引...")
        idx_next_review = Index('ix_progress_next_review', Progress.next_review)
        idx_next_review.create(engine)
        print("✅ next_review 索引创建成功")
    else:
        print("ℹ️  next_review 索引已存在")
    
    # 添加 error_count 索引
    if not check_index_exists(inspector, 'progress', 'ix_progress_error_count'):
        print("添加 error_count 索引...")
        idx_error_count = Index('ix_progress_error_count', Progress.error_count)
        idx_error_count.create(engine)
        print("✅ error_count 索引创建成功")
    else:
        print("ℹ️  error_count 索引已存在")
    
    print("性能索引迁移完成！")

def add_new_columns():
    """添加新列（如果不存在）"""
    print("\n检查新增列...")
    
    db = SessionLocal()
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('progress')]
        
        # 检查 last_reviewed 列
        if 'last_reviewed' not in columns:
            print("添加 last_reviewed 列...")
            with engine.connect() as conn:
                conn.execute(text('ALTER TABLE progress ADD COLUMN last_reviewed DATE'))
                conn.commit()
            print("✅ last_reviewed 列创建成功")
        else:
            print("ℹ️  last_reviewed 列已存在")
        
        # 检查 review_count 列
        if 'review_count' not in columns:
            print("添加 review_count 列...")
            with engine.connect() as conn:
                conn.execute(text('ALTER TABLE progress ADD COLUMN review_count INTEGER DEFAULT 0'))
                conn.commit()
            print("✅ review_count 列创建成功")
        else:
            print("ℹ️  review_count 列已存在")
        
    except Exception as e:
        print(f"❌ 添加列时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    print("=" * 50)
    print("数据库性能优化迁移")
    print("=" * 50)
    
    try:
        add_new_columns()
        add_performance_indexes()
        print("\n✅ 迁移全部完成！")
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        sys.exit(1)
