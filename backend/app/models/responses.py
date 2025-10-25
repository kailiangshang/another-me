"""
API 响应数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = Field(True, description="请求是否成功")
    message: str = Field("", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field("ok", description="服务状态")
    version: str = Field("1.0.0", description="API 版本")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    message: str = Field(..., description="AI 回复")
    timestamp: datetime = Field(default_factory=datetime.now)


class DocumentInfo(BaseModel):
    """文档信息模型"""
    id: str = Field(..., description="文档 ID")
    filename: str = Field(..., description="文件名")
    size: int = Field(..., description="文件大小（字节）")
    upload_time: datetime = Field(default_factory=datetime.now)
    chunk_count: Optional[int] = Field(None, description="分块数量")


class UploadResponse(BaseModel):
    """上传响应模型"""
    success: bool = True
    document_id: str = Field(..., description="文档 ID")
    filename: str
    message: str = "Document uploaded successfully"


class SearchResult(BaseModel):
    """检索结果模型"""
    content: str = Field(..., description="内容")
    score: float = Field(..., description="相似度分数")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class SearchResponse(BaseModel):
    """检索响应模型"""
    query: str
    results: List[SearchResult]
    total: int = Field(..., description="结果总数")


class RAGStats(BaseModel):
    """RAG 统计信息"""
    document_count: int = Field(0, description="文档总数")
    total_chunks: int = Field(0, description="总分块数")
    total_size: int = Field(0, description="总大小（字节）")


class Memory(BaseModel):
    """记忆模型"""
    id: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryListResponse(BaseModel):
    """记忆列表响应"""
    memories: List[Memory]
    total: int


class ConfigTestResult(BaseModel):
    """配置测试结果"""
    success: bool
    message: str
    model_available: Optional[bool] = None


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    error: str = Field(..., description="错误信息")
    detail: Optional[str] = Field(None, description="详细错误")
    timestamp: datetime = Field(default_factory=datetime.now)
