"""
缓存管理模块
提供统一的缓存接口
"""

import time
from typing import Any, Optional, Callable
from functools import wraps
import json
import hashlib


class CacheManager:
    """内存缓存管理器"""
    
    def __init__(self, default_ttl: int = 3600):
        """
        Args:
            default_ttl: 默认过期时间（秒）
        """
        self._cache = {}
        self._expiry = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key not in self._cache:
            return None
        
        # 检查是否过期
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._cache[key]
            del self._expiry[key]
            return None
        
        return self._cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存"""
        self._cache[key] = value
        
        if ttl is None:
            ttl = self.default_ttl
        
        if ttl > 0:
            self._expiry[key] = time.time() + ttl
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expiry:
            del self._expiry[key]
    
    def clear(self):
        """清空所有缓存"""
        self._cache.clear()
        self._expiry.clear()
    
    def get_stats(self) -> dict:
        """获取缓存统计"""
        return {
            "total_keys": len(self._cache),
            "expired_keys": sum(
                1 for k, exp in self._expiry.items()
                if time.time() > exp
            )
        }


# 全局缓存实例
cache_manager = CacheManager(default_ttl=1800)  # 30分钟


def cached(ttl: int = 1800, key_func: Optional[Callable] = None):
    """
    缓存装饰器
    
    Args:
        ttl: 缓存时间（秒）
        key_func: 自定义key生成函数
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # 默认使用函数名和参数生成key
                key_data = {
                    "func": func.__name__,
                    "args": str(args),
                    "kwargs": str(sorted(kwargs.items()))
                }
                cache_key = hashlib.md5(
                    json.dumps(key_data).encode()
                ).hexdigest()
            
            # 尝试从缓存获取
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 保存到缓存
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
