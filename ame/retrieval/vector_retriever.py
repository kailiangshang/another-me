"""
向量检索器 - 基于向量相似度的检索
"""

from typing import List, Dict, Any, Optional
from .base import RetrieverBase, RetrievalResult
from ame.vector_store.base import VectorStoreBase


class VectorRetriever(RetrieverBase):
    """向量检索器"""
    
    def __init__(self, vector_store: VectorStoreBase):
        """
        初始化向量检索器
        
        Args:
            vector_store: 向量存储实例
        """
        self.vector_store = vector_store
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[RetrievalResult]:
        """
        使用向量相似度检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filters: 过滤条件（如时间范围、来源等）
            **kwargs: 其他参数
                - min_score: 最小相似度阈值
                - embedding_model: 自定义嵌入模型
        """
        # 从向量存储中搜索
        results = await self.vector_store.search(
            query=query,
            limit=top_k,
            filter=filters
        )
        
        # 转换为统一的检索结果格式
        retrieval_results = []
        for item in results:
            retrieval_results.append(
                RetrievalResult(
                    content=item.get("content", ""),
                    metadata=item.get("metadata", {}),
                    score=item.get("similarity", 0.0),
                    source="vector"
                )
            )
        
        # 应用最小分数过滤
        min_score = kwargs.get("min_score", 0.0)
        if min_score > 0:
            retrieval_results = [r for r in retrieval_results if r.score >= min_score]
        
        return retrieval_results
    
    def get_name(self) -> str:
        return "VectorRetriever"
