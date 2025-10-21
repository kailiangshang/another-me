"""
检索器抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    """检索结果"""
    content: str
    metadata: Dict[str, Any]
    score: float
    source: str = ""
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "metadata": self.metadata,
            "score": self.score,
            "source": self.source
        }


class RetrieverBase(ABC):
    """检索器抽象基类"""
    
    @abstractmethod
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[RetrievalResult]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filters: 过滤条件
            **kwargs: 其他参数
            
        Returns:
            检索结果列表
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取检索器名称"""
        pass
    
    def post_process(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """
        后处理检索结果（可选）
        
        Args:
            results: 原始检索结果
            
        Returns:
            处理后的结果
        """
        return results
