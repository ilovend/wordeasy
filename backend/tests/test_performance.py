"""
性能测试和基准测试
"""
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models, crud

# 使用测试数据库
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./benchmark.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_test_data(db, num_words=1000):
    """创建测试数据"""
    print(f"创建 {num_words} 个测试单词...")
    words = []
    for i in range(num_words):
        word = models.Word(
            word=f"word{i:04d}",
            zh_definition=f"测试单词{i}",
            difficulty=(i % 3) + 1,
            category="性能测试"
        )
        words.append(word)
    
    db.bulk_save_objects(words)
    db.commit()
    print(f"✓ 已创建 {num_words} 个测试单词")

def benchmark_get_words(db, iterations=100):
    """基准测试：获取单词列表"""
    print(f"\n测试 get_words_by_difficulty ({iterations} 次迭代)...")
    
    start_time = time.time()
    for _ in range(iterations):
        words = crud.get_words_by_difficulty(db, difficulty=1, limit=10)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations * 1000
    print(f"平均响应时间: {avg_time:.2f}ms")
    
    if avg_time > 50:
        print(f"⚠ 警告: 响应时间超过50ms")
    else:
        print(f"✓ 性能良好")
    
    return avg_time

def benchmark_get_review_words(db, iterations=100):
    """基准测试：获取复习单词"""
    print(f"\n测试 get_review_words ({iterations} 次迭代)...")
    
    # 创建一些进度记录
    words = crud.get_words_by_difficulty(db, difficulty=1, limit=20)
    for word in words[:10]:
        crud.get_or_create_progress(db, word.id)
    
    start_time = time.time()
    for _ in range(iterations):
        review_words = crud.get_review_words(db, limit=20)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations * 1000
    print(f"平均响应时间: {avg_time:.2f}ms")
    
    if avg_time > 50:
        print(f"⚠ 警告: 响应时间超过50ms")
    else:
        print(f"✓ 性能良好")
    
    return avg_time

def benchmark_get_error_words(db, iterations=100):
    """基准测试：获取错词"""
    print(f"\n测试 get_error_words ({iterations} 次迭代)...")
    
    # 创建一些错误记录
    words = crud.get_words_by_difficulty(db, difficulty=1, limit=20)
    for word in words[:10]:
        progress = crud.get_or_create_progress(db, word.id)
        progress.error_count = 5
    db.commit()
    
    start_time = time.time()
    for _ in range(iterations):
        error_words = crud.get_error_words(db, limit=20)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations * 1000
    print(f"平均响应时间: {avg_time:.2f}ms")
    
    if avg_time > 50:
        print(f"⚠ 警告: 响应时间超过50ms")
    else:
        print(f"✓ 性能良好")
    
    return avg_time

def benchmark_update_progress(db, iterations=100):
    """基准测试：更新进度"""
    print(f"\n测试 update_progress ({iterations} 次迭代)...")
    
    words = crud.get_words_by_difficulty(db, difficulty=1, limit=10)
    word_id = words[0].id
    
    start_time = time.time()
    for i in range(iterations):
        crud.update_progress(db, word_id, is_correct=(i % 2 == 0))
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations * 1000
    print(f"平均响应时间: {avg_time:.2f}ms")
    
    if avg_time > 20:
        print(f"⚠ 警告: 响应时间超过20ms")
    else:
        print(f"✓ 性能良好")
    
    return avg_time

def run_all_benchmarks():
    """运行所有基准测试"""
    print("="*60)
    print("WordEasy 性能基准测试")
    print("="*60)
    
    # 创建数据库
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 设置测试数据
        setup_test_data(db, num_words=1000)
        
        # 运行基准测试
        results = {
            "get_words": benchmark_get_words(db, iterations=100),
            "get_review_words": benchmark_get_review_words(db, iterations=100),
            "get_error_words": benchmark_get_error_words(db, iterations=100),
            "update_progress": benchmark_update_progress(db, iterations=100)
        }
        
        # 总结
        print("\n" + "="*60)
        print("性能测试总结")
        print("="*60)
        for test_name, avg_time in results.items():
            status = "✓" if avg_time < 50 else "⚠"
            print(f"{status} {test_name}: {avg_time:.2f}ms")
        
        # 整体评分
        overall_avg = sum(results.values()) / len(results)
        print(f"\n平均响应时间: {overall_avg:.2f}ms")
        
        if overall_avg < 30:
            print("✓ 整体性能: 优秀")
        elif overall_avg < 50:
            print("✓ 整体性能: 良好")
        elif overall_avg < 100:
            print("⚠ 整体性能: 一般")
        else:
            print("⚠ 整体性能: 需要优化")
        
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        print("\n✓ 清理完成")

if __name__ == "__main__":
    run_all_benchmarks()
