"""
中间件模块
提供请求日志、性能监控、错误追踪等功能
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import json
from .logger import get_logger

logger = get_logger("middleware")


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 添加响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            # 记录响应
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"Status: {response.status_code} Time: {process_time:.3f}s"
            )
            
            return response
        
        except Exception as e:
            # 记录错误
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url.path} "
                f"Error: {str(e)} Time: {process_time:.3f}s",
                exc_info=True
            )
            raise


class PerformanceMonitorMiddleware(BaseHTTPMiddleware):
    """性能监控中间件"""
    
    def __init__(self, app: ASGIApp, slow_threshold: float = 1.0):
        """
        Args:
            app: ASGI 应用
            slow_threshold: 慢请求阈值（秒）
        """
        super().__init__(app)
        self.slow_threshold = slow_threshold
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # 记录慢请求
        if process_time > self.slow_threshold:
            logger.warning(
                f"Slow Request: {request.method} {request.url.path} "
                f"Time: {process_time:.3f}s"
            )
        
        return response


class ErrorTrackingMiddleware(BaseHTTPMiddleware):
    """错误追踪中间件"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # 详细的错误信息
            error_details = {
                "path": str(request.url.path),
                "method": request.method,
                "error": str(e),
                "type": type(e).__name__,
            }
            
            logger.error(
                f"Unhandled Exception: {json.dumps(error_details, ensure_ascii=False)}",
                exc_info=True
            )
            
            # 重新抛出异常，让 FastAPI 的异常处理器处理
            raise
