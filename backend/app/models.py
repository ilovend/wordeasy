"""
SQLAlchemy数据库模型
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date

class Word(Base):
    """单词表"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, unique=True, nullable=False, index=True)
    zh_definition = Column(String, nullable=False)
    difficulty = Column(Integer, CheckConstraint('difficulty BETWEEN 1 AND 3'), nullable=False)
    category = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    
    # 关系
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
