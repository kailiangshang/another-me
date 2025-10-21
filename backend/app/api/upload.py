from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.upload_service import UploadService

router = APIRouter()
upload_service = UploadService()


@router.post("/files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    上传数据文件（聊天记录、日记、图片等）
    """
    try:
        results = await upload_service.process_uploads(files)
        return {
            "status": "success",
            "uploaded": len(results),
            "files": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text")
async def upload_text(content: dict):
    """
    直接上传文本内容
    """
    try:
        result = await upload_service.process_text(
            content.get("text", ""),
            content.get("source", "manual"),
            content.get("timestamp")
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_upload_status():
    """
    获取上传数据统计
    """
    return await upload_service.get_statistics()
