from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.config_service import ConfigService

router = APIRouter()
config_service = ConfigService()


class APIConfig(BaseModel):
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-3.5-turbo"


@router.post("/api-key")
async def update_api_config(config: APIConfig):
    """
    配置 OpenAI Compatible API
    """
    try:
        result = await config_service.update_api_config(
            api_key=config.api_key,
            base_url=config.base_url,
            model=config.model
        )
        return {"status": "success", "message": "API 配置已更新"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-key")
async def get_api_config():
    """
    获取当前 API 配置（隐藏敏感信息）
    """
    config = await config_service.get_api_config()
    return {
        "base_url": config.get("base_url"),
        "model": config.get("model"),
        "api_key_set": bool(config.get("api_key"))
    }
