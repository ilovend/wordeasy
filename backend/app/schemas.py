"""
Pydantic模型定义（API输入输出）
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date

class WordBase(BaseModel):
    word: str
    zh_definition: str
    difficulty: int
    category: Optional[str] = None
    audio_url: Optional[str] = None

class WordCreate(WordBase):
    pass

class WordResponse(WordBase):
    id: int
    mastery_level: Optional[int] = 0
    next_review: Optional[date] = None
    error_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class SpellCheckRequest(BaseModel):
    word_id: int
    input: str

class SpellCheckResponse(BaseModel):
    correct: bool
    correct_word: str
    next_review: Optional[date] = None
    mastery_level: int

class ProgressResponse(BaseModel):
    level: int
    coins: int
    mastery: dict  # {"红": 5, "黄": 10, "绿": 15}

class UploadResponse(BaseModel):
    status: str
    count: int
    message: Optional[str] = None

class MarkStudiedRequest(BaseModel):
    word_id: int

class BatchUpdateRequest(BaseModel):
    word_ids: list[int]
