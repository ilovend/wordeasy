"""
缓存工具
提供简单的内存缓存功能
"""
from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Callable, Optional
import hashlib
import json

class SimpleCache:
    """简单的内存缓存"""
    
    def __init__(self):
        self._cache = {}
        self._expire_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self._cache:
            return None
        
        # 检查是否过期
        if key in self._expire_times:
            if datetime.now() > self._expire_times[key]:
                self.delete(key)
                return None
        
        return self._cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None表示永不过期
        """
        self._cache[key] = value
        
        if ttl:
            self._expire_times[key] = datetime.now() + timedelta(seconds=ttl)
        elif key in self._expire_times:
            del self._expire_times[key]
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expire_times:
            del self._expire_times[key]
    
    def clear(self):
        """清空所有缓存"""
        self._cache.clear()
        self._expire_times.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self._cache)

# 全局缓存实例
cache = SimpleCache()

def cached(ttl: int = 300, key_prefix: str = ""):
    """缓存装饰器
    
    Args:
        ttl: 缓存时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [key_prefix, func.__name__]
            
            # 添加参数到键中
            if args:
                key_parts.append(str(args))
            if kwargs:
                key_parts.append(json.dumps(kwargs, sort_keys=True))
            
            cache_key = hashlib.md5(
                "_".join(key_parts).encode()
            ).hexdigest()
            
            # 尝试从缓存获取
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
