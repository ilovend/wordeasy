"""
SQLAlchemy数据库模型
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date

class Deck(Base):
    """词库（卡组）表"""
    __tablename__ = "decks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    daily_new_limit = Column(Integer, default=100)
    new_batch_size = Column(Integer, default=30)
    target_language = Column(String, default="英语")
    voice_type = Column(String, default="默认")
    deck_type = Column(String, default="单词库")
    algorithm = Column(String, default="FSRS")
    new_priority = Column(String, default="默认")
    review_priority = Column(String, default="默认")
    duplicate_filter = Column(String, default="过滤")
    total_words = Column(Integer, default=0)
    learned_words = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=date.today)
    
    # 关系
    words = relationship("Word", back_populates="deck")

class Word(Base):
    """单词表"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, nullable=False, index=True)
    zh_definition = Column(String, nullable=False)
    difficulty = Column(Integer, CheckConstraint('difficulty BETWEEN 1 AND 3'), nullable=False)
    category = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False, default=1, index=True)
    created_at = Column(Date, default=date.today)
    
    # 关系
    deck = relationship("Deck", back_populates="words")
    progress = relationship("Progress", back_populates="word", uselist=False)

class Progress(Base):
    """学习进度表"""
    __tablename__ = "progress"
    
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    mastery_level = Column(Integer, default=0)  # 0陌生/1熟悉/2掌握
    next_review = Column(Date, nullable=True, index=True)  # 添加索引以优化复习查询
    error_count = Column(Integer, default=0, index=True)  # 添加索引以优化错词查询
    last_reviewed = Column(Date, nullable=True)  # 最后复习日期
    review_count = Column(Integer, default=0)  # 复习次数
    
    # 关系
    word = relationship("Word", back_populates="progress")
