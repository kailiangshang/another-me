from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()


class MemoryRequest(BaseModel):
    query: str
    time_context: Optional[str] = None  # e.g., "2020-03", "去年这个时候"
    limit: int = 5


@router.post("/recall")
async def recall_memories(request: MemoryRequest):
    """
    业务功能 3: 记忆回溯对话
    
    唤醒遗忘的记忆，实现时空对话
    """
    try:
        memories = await memory_service.recall(
            query=request.query,
            time_context=request.time_context,
            limit=request.limit
        )
        return {
            "status": "success",
            "memories": memories["items"],
            "summary": memories.get("summary", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline")
async def get_timeline(year: Optional[int] = None, month: Optional[int] = None):
    """
    获取时间线视图
    """
    try:
        timeline = await memory_service.get_timeline(year=year, month=month)
        return {"status": "success", "timeline": timeline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/similar")
async def find_similar_moments(request: MemoryRequest):
    """
    查找相似的历史时刻
    """
    try:
        similar = await memory_service.find_similar(
            query=request.query,
            limit=request.limit
        )
        return {"status": "success", "similar_moments": similar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
