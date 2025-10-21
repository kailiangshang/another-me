"""
性能监控工具
"""

import time
from functools import wraps
from app.core.logger import get_logger

logger = get_logger("performance")


def performance_monitor(threshold: float = 1.0):
    """
    性能监控装饰器
    
    Args:
        threshold: 慢函数阈值（秒）
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start_time
                
                if elapsed > threshold:
                    logger.warning(
                        f"Slow function: {func.__name__} "
                        f"took {elapsed:.3f}s (threshold: {threshold}s)"
                    )
                else:
                    logger.debug(
                        f"Function {func.__name__} "
                        f"took {elapsed:.3f}s"
                    )
        
        return wrapper
    return decorator


class PerformanceTimer:
    """性能计时器上下文管理器"""
    
    def __init__(self, name: str, threshold: float = 1.0):
        """
        Args:
            name: 操作名称
            threshold: 慢操作阈值
        """
        self.name = name
        self.threshold = threshold
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        
        if elapsed > self.threshold:
            logger.warning(
                f"Slow operation: {self.name} "
                f"took {elapsed:.3f}s"
            )
        else:
            logger.debug(
                f"Operation {self.name} "
                f"took {elapsed:.3f}s"
            )
