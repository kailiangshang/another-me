from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.mimic_service import MimicService

router = APIRouter()
mimic_service = MimicService()


class MimicRequest(BaseModel):
    prompt: str
    context: str = ""
    temperature: float = 0.7


@router.post("/chat")
async def mimic_chat(request: MimicRequest):
    """
    业务功能 1: 模仿我说话
    
    让 AI 用你的语气、风格和思维方式回应问题
    """
    try:
        response = await mimic_service.generate_response(
            prompt=request.prompt,
            context=request.context,
            temperature=request.temperature
        )
        return {
            "status": "success",
            "response": response["text"],
            "metadata": {
                "references": response.get("references", []),
                "confidence": response.get("confidence", 0.0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-post")
async def generate_social_post(request: MimicRequest):
    """
    生成社交媒体帖子（朋友圈、微博等）
    """
    try:
        response = await mimic_service.generate_social_post(
            topic=request.prompt,
            context=request.context
        )
        return {"status": "success", "post": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
