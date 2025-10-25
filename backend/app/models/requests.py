"""
API 请求数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息")
    context: Optional[str] = Field(None, description="对话上下文")


class LearnRequest(BaseModel):
    """学习请求模型"""
    message: str = Field(..., description="要学习的消息")
    context: Optional[str] = Field(None, description="消息上下文")


class SearchRequest(BaseModel):
    """检索请求模型"""
    query: str = Field(..., description="检索查询")
    top_k: int = Field(5, description="返回结果数量")


class ConfigRequest(BaseModel):
    """配置请求模型"""
    api_key: str = Field(..., description="OpenAI API Key")
    base_url: Optional[str] = Field("https://api.openai.com/v1", description="API 基础 URL")
    model: Optional[str] = Field("gpt-3.5-turbo", description="模型名称")


class ConfigTestRequest(BaseModel):
    """配置测试请求模型"""
    api_key: str
    base_url: str
    model: str
