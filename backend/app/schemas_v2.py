"""
增强版 Pydantic Schema - 支持词库分类管理
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

# 枚举类型
class LanguageType(str, Enum):
    ENGLISH = "英语"
    JAPANESE = "日语"
    CHINESE = "中文(普通话)"
    KOREAN = "韩语"
    GERMAN = "德语"
    FRENCH = "法语"
    SPANISH = "西班牙语"

class VoiceType(str, Enum):
    DEFAULT = "默认"
    US = "美音"
    UK = "英音"
    NATIVE = "母语"

class DeckType(str, Enum):
    VOCABULARY = "单词库"
    COURSE = "课程库"
    CUSTOM = "自定义"

class AlgorithmType(str, Enum):
    FSRS = "FSRS"
    STEP_MASTER = "StepMaster"
    SM2 = "SM-2"

class PriorityType(str, Enum):
    DEFAULT = "默认"
    RANDOM = "随机"

class DuplicateFilter(str, Enum):
    FILTER = "过滤"
    ALLOW = "允许"

# 词库相关
class DeckCreate(BaseModel):
    """创建词库"""
    name: str = Field(..., min_length=1, max_length=100, description="词库名称")
    description: Optional[str] = Field(None, max_length=500, description="词库描述")
    daily_new_limit: int = Field(100, ge=1, le=1000, description="每日新学数量")
    new_batch_size: int = Field(30, ge=1, le=100, description="新学批次数量")
    target_language: LanguageType = Field(LanguageType.ENGLISH, description="目标语言")
    voice_type: VoiceType = Field(VoiceType.DEFAULT, description="发音人")
    deck_type: DeckType = Field(DeckType.VOCABULARY, description="词库类型")
    algorithm: AlgorithmType = Field(AlgorithmType.FSRS, description="记忆算法")
    new_priority: PriorityType = Field(PriorityType.DEFAULT, description="新学优先级")
    review_priority: PriorityType = Field(PriorityType.DEFAULT, description="复习优先级")
    duplicate_filter: DuplicateFilter = Field(DuplicateFilter.FILTER, description="重复过滤")

class DeckUpdate(BaseModel):
    """更新词库"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    daily_new_limit: Optional[int] = Field(None, ge=1, le=1000)
    new_batch_size: Optional[int] = Field(None, ge=1, le=100)
    target_language: Optional[LanguageType] = None
    voice_type: Optional[VoiceType] = None
    deck_type: Optional[DeckType] = None
    algorithm: Optional[AlgorithmType] = None
    new_priority: Optional[PriorityType] = None
    review_priority: Optional[PriorityType] = None
    duplicate_filter: Optional[DuplicateFilter] = None
    is_active: Optional[bool] = None

class DeckResponse(BaseModel):
    """词库响应"""
    id: int
    name: str
    description: Optional[str]
    daily_new_limit: int
    new_batch_size: int
    target_language: LanguageType
    voice_type: VoiceType
    deck_type: DeckType
    algorithm: AlgorithmType
    new_priority: PriorityType
    review_priority: PriorityType
    duplicate_filter: DuplicateFilter
    total_words: int
    learned_words: int
    is_active: bool
    created_at: date
    
    class Config:
        from_attributes = True

class DeckListResponse(BaseModel):
    """词库列表响应"""
    decks: List[DeckResponse]
    total: int

# 单词相关
class WordBase(BaseModel):
    word: str
    zh_definition: str
    difficulty: int = Field(..., ge=1, le=3)
    category: Optional[str] = None
    audio_url: Optional[str] = None

class WordCreate(WordBase):
    deck_id: int  # 必须指定所属词库

class WordResponse(WordBase):
    id: int
    deck_id: int
    created_at: date
    mastery_level: Optional[int] = 0
    next_review: Optional[date] = None
    error_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class WordWithDeck(WordResponse):
    """带词库信息的单词"""
    deck_name: str
    deck_type: DeckType

# 批量上传
class UploadWordsRequest(BaseModel):
    """批量上传单词到指定词库"""
    deck_id: int
    words: List[WordBase]

class UploadResponse(BaseModel):
    status: str
    count: int
    skipped: int = 0
    message: Optional[str] = None

# 学习相关
class SpellCheckRequest(BaseModel):
    word_id: int
    input: str

class SpellCheckResponse(BaseModel):
    correct: bool
    correct_word: str
    next_review: Optional[date] = None
    mastery_level: int

class MarkStudiedRequest(BaseModel):
    word_id: int

class BatchUpdateRequest(BaseModel):
    word_ids: List[int]

# 统计相关
class DeckStatsResponse(BaseModel):
    """词库统计"""
    deck_id: int
    deck_name: str
    total_words: int
    new_words: int  # 未学习
    learning_words: int  # 学习中
    mastered_words: int  # 已掌握
    due_today: int  # 今日待复习
    level1: int
    level2: int
    level3: int

class ProgressResponse(BaseModel):
    level: int
    coins: int
    mastery: dict  # {"红": 5, "黄": 10, "绿": 15}

class DailyStatsResponse(BaseModel):
    """每日学习统计"""
    date: date
    new_learned: int
    reviewed: int
    correct_count: int
    error_count: int
    accuracy: float
    study_time: int
