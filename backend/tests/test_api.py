"""
API端点测试
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# 使用内存数据库进行测试
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    """创建测试客户端"""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    """创建测试数据库会话"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # 插入测试数据
    test_words = [
        models.Word(word="test", zh_definition="测试", difficulty=1, category="测试"),
        models.Word(word="hello", zh_definition="你好", difficulty=1, category="测试"),
        models.Word(word="python", zh_definition="Python语言", difficulty=2, category="测试"),
    ]
    db.bulk_save_objects(test_words)
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_read_root(test_client):
    """测试根路径"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to WordEasy API"
    assert data["version"] == "1.3.0"

def test_get_words(test_client, test_db):
    """测试获取单词列表"""
    response = test_client.get("/api/words?difficulty=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_words_invalid_difficulty(test_client):
    """测试无效难度"""
    response = test_client.get("/api/words?difficulty=5&limit=10")
    assert response.status_code == 400
    assert "难度必须是1、2或3" in response.json()["detail"]

def test_check_spelling_correct(test_client, test_db):
    """测试正确拼写"""
    # 先获取一个单词
    words_response = test_client.get("/api/words?difficulty=1&limit=1")
    word = words_response.json()[0]
    
    # 检查正确拼写
    response = test_client.post(
        "/api/spell/check",
        json={"word_id": word["id"], "input": word["word"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is True
    assert data["correct_word"] == word["word"]

def test_check_spelling_incorrect(test_client, test_db):
    """测试错误拼写"""
    # 先获取一个单词
    words_response = test_client.get("/api/words?difficulty=1&limit=1")
    word = words_response.json()[0]
    
    # 检查错误拼写
    response = test_client.post(
        "/api/spell/check",
        json={"word_id": word["id"], "input": "wrongspelling"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is False
    assert data["correct_word"] == word["word"]

def test_get_word_stats(test_client, test_db):
    """测试词库统计"""
    response = test_client.get("/api/words/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "level1" in data
    assert "level2" in data
    assert "level3" in data
    assert data["total"] >= 0

def test_get_progress(test_client, test_db):
    """测试学习进度"""
    response = test_client.get("/api/progress")
    assert response.status_code == 200
    data = response.json()
    assert "total_words" in data
    assert "mastered" in data
    assert "familiar" in data

def test_get_review_count(test_client, test_db):
    """测试复习计数"""
    response = test_client.get("/api/progress/review-count")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "date" in data
    assert data["count"] >= 0
