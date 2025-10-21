from fastapi import APIRouter
from app.api import upload, mimic, analysis, memory, config

router = APIRouter()

# 注册各业务模块路由
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(config.router, prefix="/config", tags=["Config"])
router.include_router(mimic.router, prefix="/mimic", tags=["Mimic Me"])
router.include_router(analysis.router, prefix="/analysis", tags=["Know Myself"])
router.include_router(memory.router, prefix="/memory", tags=["Remember Me"])
