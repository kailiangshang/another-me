"""
LLM 调用器抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """LLM 响应"""
    content: str
    model: str
    usage: Dict[str, int]
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "model": self.model,
            "usage": self.usage,
            "metadata": self.metadata or {}
        }


class LLMCallerBase(ABC):
    """LLM 调用器抽象基类"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        生成回复
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            LLM响应
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        流式生成回复
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """检查是否已配置（API Key等）"""
        pass
