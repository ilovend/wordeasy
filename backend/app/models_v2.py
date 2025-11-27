"""
增强版数据库模型 - 支持词库分类管理
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date
import enum

class LanguageType(str, enum.Enum):
    """目标语言类型"""
    ENGLISH = "英语"
    JAPANESE = "日语"
    CHINESE = "中文(普通话)"
    KOREAN = "韩语"
    GERMAN = "德语"
    FRENCH = "法语"
    SPANISH = "西班牙语"

class VoiceType(str, enum.Enum):
    """发音人类型"""
    DEFAULT = "默认"
    US = "美音"
    UK = "英音"
    NATIVE = "母语"

class DeckType(str, enum.Enum):
    """词库类型"""
    VOCABULARY = "单词库"
    COURSE = "课程库"
    CUSTOM = "自定义"

class AlgorithmType(str, enum.Enum):
    """记忆算法类型"""
    FSRS = "FSRS"
    STEP_MASTER = "StepMaster"
    SM2 = "SM-2"

class PriorityType(str, enum.Enum):
    """优先级类型"""
    DEFAULT = "默认"
    RANDOM = "随机"

class DuplicateFilter(str, enum.Enum):
    """重复过滤"""
    FILTER = "过滤"
    ALLOW = "允许"

class Deck(Base):
    """词库（卡组）表"""
    __tablename__ = "decks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)  # 词库名称
    description = Column(String, nullable=True)  # 描述
    
    # 学习设置
    daily_new_limit = Column(Integer, default=100)  # 每日新学数量
    new_batch_size = Column(Integer, default=30)  # 新学批次数量
    
    # 语言设置
    target_language = Column(SQLEnum(LanguageType), default=LanguageType.ENGLISH)  # 目标语言
    voice_type = Column(SQLEnum(VoiceType), default=VoiceType.DEFAULT)  # 发音人
    
    # 词库类型
    deck_type = Column(SQLEnum(DeckType), default=DeckType.VOCABULARY)  # 库类型
    
    # 算法设置
    algorithm = Column(SQLEnum(AlgorithmType), default=AlgorithmType.FSRS)  # 记忆算法
    
    # 优先级设置
    new_priority = Column(SQLEnum(PriorityType), default=PriorityType.DEFAULT)  # 新学优先级
    review_priority = Column(SQLEnum(PriorityType), default=PriorityType.DEFAULT)  # 复习优先级
    
    # 重复过滤
    duplicate_filter = Column(SQLEnum(DuplicateFilter), default=DuplicateFilter.FILTER)  # 重复过滤
    
    # 统计信息
    total_words = Column(Integer, default=0)  # 总单词数
    learned_words = Column(Integer, default=0)  # 已学单词数
    
    # 状态
    is_active = Column(Boolean, default=True)  # 是否启用
    created_at = Column(Date, default=date.today)  # 创建日期
    
    # 关系
    words = relationship("Word", back_populates="deck")

class Word(Base):
    """单词表"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, nullable=False, index=True)  # 移除 unique 约束，允许同一单词在不同词库
    zh_definition = Column(String, nullable=False)
    difficulty = Column(Integer, CheckConstraint('difficulty BETWEEN 1 AND 3'), nullable=False)
    category = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    
    # 所属词库
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False, index=True)
    
    # 添加时间
    created_at = Column(Date, default=date.today)
    
    # 关系
    deck = relationship("Deck", back_populates="words")
    progress = relationship("Progress", back_populates="word", uselist=False)

class Progress(Base):
    """学习进度表"""
    __tablename__ = "progress"
    
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    mastery_level = Column(Integer, default=0)  # 0陌生/1熟悉/2掌握
    next_review = Column(Date, nullable=True, index=True)  # 下次复习日期
    error_count = Column(Integer, default=0, index=True)  # 错误次数
    last_reviewed = Column(Date, nullable=True)  # 最后复习日期
    review_count = Column(Integer, default=0)  # 复习次数
    
    # FSRS算法参数
    ease_factor = Column(Integer, default=250)  # 难度因子
    interval = Column(Integer, default=0)  # 间隔天数
    
    # 关系
    word = relationship("Word", back_populates="progress")

class DailyStats(Base):
    """每日学习统计"""
    __tablename__ = "daily_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False, index=True)
    stat_date = Column(Date, default=date.today, index=True)
    
    new_learned = Column(Integer, default=0)  # 新学单词数
    reviewed = Column(Integer, default=0)  # 复习单词数
    correct_count = Column(Integer, default=0)  # 正确次数
    error_count = Column(Integer, default=0)  # 错误次数
    study_time = Column(Integer, default=0)  # 学习时长（分钟）
