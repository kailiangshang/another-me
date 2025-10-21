from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.config import settings

router = APIRouter(prefix="/config", tags=["配置管理"])


class ConfigUpdate(BaseModel):
    """配置更新模型"""
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    openai_model: Optional[str] = None
    embedding_model: Optional[str] = None


class ConfigResponse(BaseModel):
    """配置响应模型"""
    is_configured: bool
    openai_base_url: str
    openai_model: str
    embedding_model: str
    has_api_key: bool  # 只返回是否有 key，不返回实际值


@router.get("/", response_model=ConfigResponse)
async def get_config():
    """获取当前配置"""
    return ConfigResponse(
        is_configured=settings.is_configured(),
        openai_base_url=settings.OPENAI_BASE_URL,
        openai_model=settings.OPENAI_MODEL,
        embedding_model=settings.EMBEDDING_MODEL,
        has_api_key=bool(settings.OPENAI_API_KEY)
    )


@router.post("/")
async def update_config(config: ConfigUpdate):
    """更新配置（运行时）"""
    try:
        config_data = {}
        
        if config.openai_api_key is not None:
            config_data['OPENAI_API_KEY'] = config.openai_api_key
        
        if config.openai_base_url is not None:
            config_data['OPENAI_BASE_URL'] = config.openai_base_url
        
        if config.openai_model is not None:
            config_data['OPENAI_MODEL'] = config.openai_model
        
        if config.embedding_model is not None:
            config_data['EMBEDDING_MODEL'] = config.embedding_model
        
        # 保存配置
        settings.save_runtime_config(config_data)
        
        return {
            "success": True,
            "message": "配置已更新",
            "is_configured": settings.is_configured()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置更新失败: {str(e)}")


@router.get("/status")
async def get_config_status():
    """获取配置状态"""
    return {
        "is_configured": settings.is_configured(),
        "has_api_key": bool(settings.OPENAI_API_KEY),
        "api_base_url": settings.OPENAI_BASE_URL,
        "model": settings.OPENAI_MODEL
    }
