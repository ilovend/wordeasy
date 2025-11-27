"""
FastAPI主应用
"""
import sys
import os

# 设置 UTF-8 编码（修复 Windows CI 环境编码问题）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import io

from . import models, schemas, crud
from .database import engine, get_db

# 创建数据库表（自动初始化）
try:
    models.Base.metadata.create_all(bind=engine)
    print("✓ 数据库表初始化成功")
except Exception as e:
    print(f"⚠ 数据库初始化警告: {e}")
    # 继续启动，因为表可能已存在

# 创建FastAPI应用
app = FastAPI(
    title="WordEasy API",
    description="拼写攻防战 - 英语单词学习API",
    version="1.4.0"
)

# CORS配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """根路径"""
    return {"message": "Welcome to WordEasy API", "version": "1.4.0"}

def _build_word_response(word: models.Word, db: Session) -> schemas.WordResponse:
    """构建单词响应对象（内部辅助函数）"""
    progress = crud.get_or_create_progress(db, word.id)
    return schemas.WordResponse(
        id=word.id,
        word=word.word,
        zh_definition=word.zh_definition,
        difficulty=word.difficulty,
        category=word.category,
        audio_url=word.audio_url,
        mastery_level=progress.mastery_level,
        next_review=progress.next_review,
        error_count=progress.error_count
    )

@app.get("/api/words", response_model=List[schemas.WordResponse])
def get_words(difficulty: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取指定难度的单词列表
    - difficulty: 1初级/2中级/3高级
    - limit: 返回单词数量
    """
    if difficulty not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="难度必须是1、2或3")
    
    words = crud.get_words_by_difficulty(db, difficulty, limit)
    return [_build_word_response(word, db) for word in words]

@app.get("/api/words/review", response_model=List[schemas.WordResponse])
def get_review_words(limit: int = 20, db: Session = Depends(get_db)):
    """获取今日待复习单词"""
    words = crud.get_review_words(db, limit)
    return [_build_word_response(word, db) for word in words]

@app.get("/api/words/errors", response_model=List[schemas.WordResponse])
def get_error_words(limit: int = 20, db: Session = Depends(get_db)):
    """获取错词本"""
    words = crud.get_error_words(db, limit)
    return [_build_word_response(word, db) for word in words]

@app.post("/api/spell/check", response_model=schemas.SpellCheckResponse)
def check_spelling(request: schemas.SpellCheckRequest, db: Session = Depends(get_db)):
    """检查拼写是否正确（优化：添加输入验证）"""
    word = crud.get_word_by_id(db, request.word_id)
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    
    # 标准化输入：去除空白、转小写
    user_input = request.input.strip().lower()
    correct_word = word.word.lower()
    
    # 判断是否正确
    is_correct = user_input == correct_word
    
    # 更新进度
    progress = crud.update_progress(db, request.word_id, is_correct)
    
    return schemas.SpellCheckResponse(
        correct=is_correct,
        correct_word=word.word,
        next_review=progress.next_review,
        mastery_level=progress.mastery_level
    )

@app.get("/api/progress", response_model=schemas.ProgressResponse)
def get_progress(db: Session = Depends(get_db)):
    """获取学习进度统计"""
    stats = crud.get_progress_stats(db)
    return schemas.ProgressResponse(**stats)

@app.get("/api/words/stats")
def get_word_stats(db: Session = Depends(get_db)):
    """获取词库统计信息"""
    level1_count = db.query(models.Word).filter(models.Word.difficulty == 1).count()
    level2_count = db.query(models.Word).filter(models.Word.difficulty == 2).count()
    level3_count = db.query(models.Word).filter(models.Word.difficulty == 3).count()
    total_count = db.query(models.Word).count()
    
    return {
        "level1": level1_count,
        "level2": level2_count,
        "level3": level3_count,
        "total": total_count
    }

@app.post("/api/words/reclassify")
def reclassify_words(db: Session = Depends(get_db)):
    """重新智能分类所有自定义词库的难度"""
    try:
        from .word_classifier import classify_word_difficulty
        
        # 获取所有自定义单词
        custom_words = db.query(models.Word).filter(
            models.Word.category == "自定义"
        ).all()
        
        if not custom_words:
            return {
                "status": "info",
                "message": "没有需要重新分类的自定义单词",
                "updated": 0
            }
        
        # 批量重新分类
        updated_count = 0
        difficulty_stats = {1: 0, 2: 0, 3: 0}
        
        for word in custom_words:
            new_difficulty = classify_word_difficulty(word.word)
            difficulty_stats[new_difficulty] += 1
            
            if word.difficulty != new_difficulty:
                word.difficulty = new_difficulty
                updated_count += 1
        
        if updated_count > 0:
            db.commit()
        
        # 获取最新统计
        stats = {
            "level1": db.query(models.Word).filter(models.Word.difficulty == 1).count(),
            "level2": db.query(models.Word).filter(models.Word.difficulty == 2).count(),
            "level3": db.query(models.Word).filter(models.Word.difficulty == 3).count()
        }
        
        return {
            "status": "success",
            "message": f"重新分类完成！更新了 {updated_count} 个单词 (初级:{difficulty_stats[1]} 中级:{difficulty_stats[2]} 高级:{difficulty_stats[3]})",
            "updated": updated_count,
            "stats": stats
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"重新分类失败: {str(e)}")

@app.post("/api/words/format")
def format_words(db: Session = Depends(get_db)):
    """清空词库：删除所有单词数据"""
    try:
        word_count = db.query(models.Word).count()
        
        if word_count == 0:
            return {
                "status": "info",
                "message": "词库已经是空的",
                "deleted_count": 0
            }
        
        # 删除所有单词
        db.query(models.Word).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": f"词库已清空，共删除 {word_count} 个单词",
            "deleted_count": word_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"清空词库失败: {str(e)}")

@app.post("/api/progress/clear")
def clear_progress(db: Session = Depends(get_db)):
    """清理学习进度：重置所有单词的学习记录和错误计数"""
    try:
        progress_count = db.query(models.Progress).count()
        
        if progress_count == 0:
            return {
                "status": "info",
                "message": "没有学习进度记录",
                "cleared_count": 0
            }
        
        # 删除所有学习进度记录
        db.query(models.Progress).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": f"学习进度已清理，共重置 {progress_count} 条记录",
            "cleared_count": progress_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"清理进度失败: {str(e)}")

@app.post("/api/progress/mark-studied")
def mark_word_studied(request: schemas.MarkStudiedRequest, db: Session = Depends(get_db)):
    """标记单词为已学习（学习模式专用）"""
    word = crud.get_word_by_id(db, request.word_id)
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    
    # 创建或更新进度，标记为已学习（不算答对，只是看过了）
    progress = crud.get_or_create_progress(db, request.word_id)
    
    # 设置下次复习时间为明天
    from datetime import date, timedelta
    progress.next_review = date.today() + timedelta(days=1)
    db.commit()
    db.refresh(progress)
    
    return {
        "status": "success",
        "message": "已标记为学习",
        "next_review": progress.next_review
    }

@app.post("/api/progress/batch-update")
def batch_update_progress(request: schemas.BatchUpdateRequest, db: Session = Depends(get_db)):
    """批量更新学习进度（用于学习模式结束时）"""
    try:
        updated_count = 0
        from datetime import date, timedelta
        
        for word_id in request.word_ids:
            word = crud.get_word_by_id(db, word_id)
            if not word:
                continue
            
            progress = crud.get_or_create_progress(db, word_id)
            # 标记为已学习，设置明天复习
            progress.next_review = date.today() + timedelta(days=1)
            updated_count += 1
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"已更新 {updated_count} 个单词的学习记录",
            "updated_count": updated_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"批量更新失败: {str(e)}")

@app.get("/api/progress/review-count")
def get_review_count(db: Session = Depends(get_db)):
    """获取今日待复习单词数量"""
    from datetime import date
    count = db.query(models.Progress).filter(
        models.Progress.next_review <= date.today()
    ).count()
    
    return {
        "count": count,
        "date": date.today()
    }

@app.post("/api/words/upload", response_model=schemas.UploadResponse)
async def upload_words(file: UploadFile = File(...), deck_id: int = 1, db: Session = Depends(get_db)):
    """
    上传自定义词库TXT文件
    格式：每行一个单词，用|分隔英文和中文，如 "abandon|放弃"
    支持智能难度分类
    
    参数:
    - file: 上传的TXT文件
    - deck_id: 目标词库ID（默认为1，即默认词库）
    """
    # 验证文件类型
    if not file.filename.endswith('.txt') and not file.filename.endswith('.csv') and not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="仅支持TXT、CSV、JSON文件")
    
    try:
        from .word_classifier import classify_word_difficulty
        
        # 读取文件内容
        content = await file.read()
        text = content.decode('utf-8')
        lines = text.strip().split('\n')
        
        # 解析所有待添加的单词
        words_to_add = []
        invalid_lines = 0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            if '|' not in line:
                invalid_lines += 1
                continue
            
            parts = line.split('|', 1)
            if len(parts) != 2:
                invalid_lines += 1
                continue
            
            word_text = parts[0].strip().lower()
            zh_def = parts[1].strip()
            
            # 验证数据
            if not word_text or not zh_def:
                invalid_lines += 1
                continue
            
            if len(word_text) > 50 or len(zh_def) > 200:
                invalid_lines += 1
                continue
            
            # 智能分类难度
            difficulty = classify_word_difficulty(word_text)
            words_to_add.append((word_text, zh_def, difficulty))
        
        if not words_to_add:
            return schemas.UploadResponse(
                status="warning",
                count=0,
                message=f"文件中没有有效的单词（共{len(lines)}行，{invalid_lines}行无效）"
            )
        
        # 批量查询已存在的单词（在同一词库中优化：一次查询）
        word_texts = [w[0] for w in words_to_add]
        existing_words = set(
            w[0] for w in db.query(models.Word.word).filter(
                models.Word.word.in_(word_texts),
                models.Word.deck_id == deck_id
            ).all()
        )
        
        # 去重并创建新单词
        seen = set()
        new_words = []
        skip_count = 0
        difficulty_stats = {1: 0, 2: 0, 3: 0}
        
        for word_text, zh_def, difficulty in words_to_add:
            if word_text in existing_words or word_text in seen:
                skip_count += 1
                continue
            
            seen.add(word_text)
            difficulty_stats[difficulty] += 1
            new_words.append(models.Word(
                word=word_text,
                zh_definition=zh_def,
                difficulty=difficulty,
                category="自定义",
                deck_id=deck_id
            ))
        
        # 批量插入
        success_count = 0
        if new_words:
            db.bulk_save_objects(new_words)
            db.commit()
            success_count = len(new_words)
        
        # 构建响应消息
        msg_parts = [f"成功导入 {success_count} 个单词"]
        msg_parts.append(f"(初级:{difficulty_stats[1]} 中级:{difficulty_stats[2]} 高级:{difficulty_stats[3]})")
        
        if skip_count > 0:
            msg_parts.append(f"，跳过 {skip_count} 个重复")
        if invalid_lines > 0:
            msg_parts.append(f"，忽略 {invalid_lines} 行无效数据")
        
        return schemas.UploadResponse(
            status="success",
            count=success_count,
            message=''.join(msg_parts)
        )
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="文件编码错误，请使用UTF-8编码")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
