"""
检索器工厂 - 创建和配置检索器
"""

from typing import Optional
from .base import RetrieverBase
from .vector_retriever import VectorRetriever
from .hybrid_retriever import HybridRetriever
from .reranker import Reranker, LLMReranker, RerankerBase
from ame.vector_store.base import VectorStoreBase


class RetrieverFactory:
    """检索器工厂类"""
    
    @staticmethod
    def create_retriever(
        retriever_type: str,
        vector_store: VectorStoreBase,
        **kwargs
    ) -> RetrieverBase:
        """
        创建检索器
        
        Args:
            retriever_type: 检索器类型
                - vector: 纯向量检索
                - hybrid: 混合检索（向量+关键词+时间）
            vector_store: 向量存储实例
            **kwargs: 其他参数
                - vector_weight: 向量权重（hybrid）
                - keyword_weight: 关键词权重（hybrid）
                - time_weight: 时间权重（hybrid）
                
        Returns:
            检索器实例
        """
        if retriever_type == "vector":
            return VectorRetriever(vector_store=vector_store)
        
        elif retriever_type == "hybrid":
            vector_retriever = VectorRetriever(vector_store=vector_store)
            return HybridRetriever(
                vector_retriever=vector_retriever,
                vector_weight=kwargs.get("vector_weight", 0.7),
                keyword_weight=kwargs.get("keyword_weight", 0.2),
                time_weight=kwargs.get("time_weight", 0.1)
            )
        
        else:
            raise ValueError(f"Unknown retriever type: {retriever_type}")
    
    @staticmethod
    def create_reranker(
        reranker_type: str = "diversity",
        llm_caller=None
    ) -> RerankerBase:
        """
        创建重排序器
        
        Args:
            reranker_type: 重排序器类型
                - diversity: 多样性优先
                - relevance: 相关性优先
                - recency: 时效性优先
                - llm: 基于LLM的重排序
            llm_caller: LLM调用器（仅llm类型需要）
            
        Returns:
            重排序器实例
        """
        if reranker_type == "llm":
            if not llm_caller:
                raise ValueError("LLM reranker requires llm_caller")
            return LLMReranker(llm_caller=llm_caller)
        else:
            return Reranker(strategy=reranker_type)
