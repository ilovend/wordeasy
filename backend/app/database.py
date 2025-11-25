"""
数据库配置和连接管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "wordeasy.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite需要此配置
)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
