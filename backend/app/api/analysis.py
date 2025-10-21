from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.analysis_service import AnalysisService

router = APIRouter()
analysis_service = AnalysisService()


class AnalysisRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    analysis_type: str = "comprehensive"  # comprehensive, emotion, keywords, relationships


@router.post("/report")
async def generate_analysis_report(request: AnalysisRequest):
    """
    业务功能 2: 自我认知分析
    
    生成自我认知分析报告
    """
    try:
        report = await analysis_service.generate_report(
            start_date=request.start_date,
            end_date=request.end_date,
            analysis_type=request.analysis_type
        )
        return {"status": "success", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/emotions")
async def get_emotion_analysis():
    """
    获取情绪分析
    """
    try:
        emotions = await analysis_service.analyze_emotions()
        return {"status": "success", "data": emotions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keywords")
async def get_keyword_analysis():
    """
    获取关键词分析（词云数据）
    """
    try:
        keywords = await analysis_service.extract_keywords()
        return {"status": "success", "data": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relationships")
async def get_relationship_analysis():
    """
    获取人际关系分析
    """
    try:
        relationships = await analysis_service.analyze_relationships()
        return {"status": "success", "data": relationships}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
