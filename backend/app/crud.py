"""
数据库CRUD操作
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from . import models, schemas
from datetime import date, timedelta
from typing import List, Optional
import random

def get_words_by_difficulty(db: Session, difficulty: int, limit: int = 10) -> List[models.Word]:
    """根据难度随机获取单词列表（优化：使用随机排序避免每次都是相同单词）"""
    total_count = db.query(models.Word).filter(models.Word.difficulty == difficulty).count()
    
    if total_count == 0:
        return []
    
    # 如果单词总数不多，直接随机打乱
    if total_count <= limit * 2:
        words = db.query(models.Word).filter(models.Word.difficulty == difficulty).all()
        random.shuffle(words)
        return words[:limit]
    
    # 随机偏移量获取不同的单词
    offset = random.randint(0, max(0, total_count - limit))
    return db.query(models.Word).filter(models.Word.difficulty == difficulty).offset(offset).limit(limit).all()

def get_word_by_id(db: Session, word_id: int) -> Optional[models.Word]:
    """根据ID获取单词"""
    return db.query(models.Word).filter(models.Word.id == word_id).first()

def get_word_by_text(db: Session, word: str) -> Optional[models.Word]:
    """根据单词文本获取单词"""
    return db.query(models.Word).filter(models.Word.word == word).first()

def create_word(db: Session, word: schemas.WordCreate) -> models.Word:
    """创建新单词"""
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

def get_or_create_progress(db: Session, word_id: int) -> models.Progress:
    """获取或创建学习进度"""
    progress = db.query(models.Progress).filter(models.Progress.word_id == word_id).first()
    if not progress:
        progress = models.Progress(word_id=word_id, mastery_level=0, next_review=date.today())
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress

def update_progress(db: Session, word_id: int, is_correct: bool) -> models.Progress:
    """更新学习进度（基于艾宾浩斯遗忘曲线）
    
    优化的遗忘曲线间隔：
    - 陌生(0): 立即复习 → 1小时 → 6小时
    - 熟悉(1): 1天 → 3天 → 7天
    - 掌握(2): 15天 → 30天
    """
    progress = get_or_create_progress(db, word_id)
    
    # 更新复习计数和最后复习日期
    progress.review_count += 1
    progress.last_reviewed = date.today()
    
    if is_correct:
        # 正确：提升掌握度并延长复习间隔
        if progress.mastery_level < 2:
            progress.mastery_level += 1
        
        # 根据掌握度设置科学的复习间隔
        intervals = {
            0: 1,    # 陌生：1天后复习
            1: 3,    # 熟悉：3天后复习
            2: 15    # 掌握：15天后复习
        }
        days = intervals.get(progress.mastery_level, 1)
        progress.next_review = date.today() + timedelta(days=days)
    else:
        # 错误：记录错误，重置复习间隔
        progress.error_count += 1
        # 错误后降低掌握度，但保留部分进度（不直接归零）
        if progress.mastery_level > 0:
            progress.mastery_level -= 1
        # 错误单词需要立即复习
        progress.next_review = date.today()
    
    db.commit()
    db.refresh(progress)
    return progress

def get_review_words(db: Session, limit: int = 20) -> List[models.Word]:
    """获取今日待复习单词（优化：按掌握度优先排序）"""
    today = date.today()
    words = db.query(models.Word).join(models.Progress).filter(
        models.Progress.next_review <= today
    ).order_by(
        models.Progress.mastery_level.asc(),  # 优先复习陌生单词
        models.Progress.error_count.desc()     # 其次是错误多的单词
    ).limit(limit).all()
    return words

def get_error_words(db: Session, limit: int = 20) -> List[models.Word]:
    """获取错词本（历史错误单词）（优化：只返回最需要复习的）"""
    words = db.query(models.Word).join(models.Progress).filter(
        models.Progress.error_count > 0
    ).order_by(
        models.Progress.error_count.desc(),
        models.Progress.mastery_level.asc()
    ).limit(limit).all()
    return words

def get_progress_stats(db: Session) -> dict:
    """获取学习进度统计"""
    # 1. 掌握度统计
    mastery_counts = db.query(
        models.Progress.mastery_level, 
        func.count(models.Progress.word_id)
    ).group_by(models.Progress.mastery_level).all()
    
    mastery_map = {0: "红", 1: "黄", 2: "绿"}
    mastery = {mastery_map.get(level, "红"): count for level, count in mastery_counts}
    
    # 2. 计算等级和积分（简单算法：掌握单词数 * 10）
    total_mastered = mastery.get("绿", 0)
    coins = total_mastered * 10
    level = min(total_mastered // 10 + 1, 99)  # 每10个掌握单词升1级
    
    # 3. 按难度的单词分布
    difficulty_counts = db.query(
        models.Word.difficulty, 
        func.count(models.Word.id)
    ).group_by(models.Word.difficulty).all()
    difficulty_distribution = {f"level{diff}": count for diff, count in difficulty_counts}
    
    # 4. 学习进度统计
    total_words = db.query(models.Word).count()
    reviewed_words = db.query(models.Progress).filter(models.Progress.review_count > 0).count()
    error_words = db.query(models.Progress).filter(models.Progress.error_count > 0).count()
    
    # 5. 最近7天的学习数据
    recent_stats = []
    for i in range(7):
        day = date.today() - timedelta(days=i)
        # 统计当天复习的单词数
        reviewed_today = db.query(models.Progress).filter(
            func.date(models.Progress.last_reviewed) == day
        ).count()
        
        recent_stats.append({
            "date": day.strftime("%m-%d"),
            "reviewed": reviewed_today
        })
    
    # 6. 错误率统计
    total_progress = db.query(models.Progress).count()
    error_rate = round((error_words / total_progress) * 100, 2) if total_progress > 0 else 0
    
    return {
        "level": level,
        "coins": coins,
        "mastery": mastery,
        "difficulty_distribution": difficulty_distribution,
        "total_words": total_words,
        "reviewed_words": reviewed_words,
        "error_words": error_words,
        "error_rate": error_rate,
        "recent_stats": recent_stats[::-1]  # 按日期升序排列
    }
