from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.core.config import settings
from app.core.middleware import LoggingMiddleware, PerformanceMonitorMiddleware, ErrorTrackingMiddleware
from app.core.logger import get_logger
import os

logger = get_logger("main")

app = FastAPI(
    title="Another Me - Backend Pipeline",
    description="隐私优先的 AI 分身系统后端",
    version="0.2.0"  # 升级版本号
)

# 创建必要的目录
os.makedirs("./logs", exist_ok=True)
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 性能监控中间件
app.add_middleware(PerformanceMonitorMiddleware, slow_threshold=2.0)

# 错误追踪中间件
app.add_middleware(ErrorTrackingMiddleware)

# 请求日志中间件
app.add_middleware(LoggingMiddleware)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Another Me API",
        "version": "0.2.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    logger.debug("Health check")
    return {"status": "healthy"}
