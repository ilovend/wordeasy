"""
性能监控工具
用于监控和记录API性能
"""
import time
from functools import wraps
from typing import Callable
import logging

logger = logging.getLogger(__name__)

def monitor_performance(func: Callable):
    """性能监控装饰器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > 1.0:  # 慢查询警告（>1秒）
                logger.warning(
                    f"Slow API call: {func.__name__} took {elapsed:.2f}s"
                )
            else:
                logger.debug(
                    f"API call: {func.__name__} took {elapsed:.3f}s"
                )
            
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"API call failed: {func.__name__} after {elapsed:.3f}s - {str(e)}"
            )
            raise
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > 1.0:
                logger.warning(
                    f"Slow operation: {func.__name__} took {elapsed:.2f}s"
                )
            else:
                logger.debug(
                    f"Operation: {func.__name__} took {elapsed:.3f}s"
                )
            
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"Operation failed: {func.__name__} after {elapsed:.3f}s - {str(e)}"
            )
            raise
    
    # 判断是否为异步函数
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

class PerformanceStats:
    """性能统计"""
    
    def __init__(self):
        self.call_counts = {}
        self.total_times = {}
        self.error_counts = {}
    
    def record_call(self, name: str, elapsed: float, error: bool = False):
        """记录调用"""
        if name not in self.call_counts:
            self.call_counts[name] = 0
            self.total_times[name] = 0.0
            self.error_counts[name] = 0
        
        self.call_counts[name] += 1
        self.total_times[name] += elapsed
        
        if error:
            self.error_counts[name] += 1
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        stats = {}
        for name in self.call_counts:
            avg_time = self.total_times[name] / self.call_counts[name]
            stats[name] = {
                'calls': self.call_counts[name],
                'total_time': round(self.total_times[name], 3),
                'avg_time': round(avg_time, 3),
                'errors': self.error_counts[name],
                'error_rate': round(
                    self.error_counts[name] / self.call_counts[name] * 100, 2
                )
            }
        return stats
    
    def reset(self):
        """重置统计"""
        self.call_counts.clear()
        self.total_times.clear()
        self.error_counts.clear()

# 全局性能统计实例
perf_stats = PerformanceStats()
