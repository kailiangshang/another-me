"""
混合检索器 - 结合多种检索策略
支持：向量检索 + 关键词检索 + 时间加权
"""

from typing import List, Dict, Any, Optional
from .base import RetrieverBase, RetrievalResult
from .vector_retriever import VectorRetriever
import re
from datetime import datetime
from collections import defaultdict


class HybridRetriever(RetrieverBase):
    """混合检索器"""
    
    def __init__(
        self,
        vector_retriever: VectorRetriever,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.2,
        time_weight: float = 0.1
    ):
        """
        初始化混合检索器
        
        Args:
            vector_retriever: 向量检索器
            vector_weight: 向量检索权重
            keyword_weight: 关键词检索权重
            time_weight: 时间权重
        """
        self.vector_retriever = vector_retriever
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight
        self.time_weight = time_weight
        
        # 归一化权重
        total = vector_weight + keyword_weight + time_weight
        self.vector_weight /= total
        self.keyword_weight /= total
        self.time_weight /= total
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[RetrievalResult]:
        """
        混合检索策略
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filters: 过滤条件
            **kwargs: 其他参数
                - keyword_boost: 关键词加权词列表
                - time_decay_days: 时间衰减天数
        """
        # 1. 向量检索
        vector_results = await self.vector_retriever.retrieve(
            query=query,
            top_k=top_k * 2,  # 取更多结果用于融合
            filters=filters
        )
        
        # 2. 关键词匹配分数
        keyword_scores = self._calculate_keyword_scores(
            query, 
            vector_results,
            boost_keywords=kwargs.get("keyword_boost", [])
        )
        
        # 3. 时间衰减分数
        time_scores = self._calculate_time_scores(
            vector_results,
            decay_days=kwargs.get("time_decay_days", 365)
        )
        
        # 4. 融合分数
        final_results = []
        for i, result in enumerate(vector_results):
            vector_score = result.score
            keyword_score = keyword_scores.get(i, 0.0)
            time_score = time_scores.get(i, 0.5)
            
            # 加权融合
            final_score = (
                self.vector_weight * vector_score +
                self.keyword_weight * keyword_score +
                self.time_weight * time_score
            )
            
            # 创建新的结果对象
            final_results.append(
                RetrievalResult(
                    content=result.content,
                    metadata={
                        **result.metadata,
                        "vector_score": vector_score,
                        "keyword_score": keyword_score,
                        "time_score": time_score
                    },
                    score=final_score,
                    source="hybrid"
                )
            )
        
        # 5. 按最终分数排序并返回 top_k
        final_results.sort(key=lambda x: x.score, reverse=True)
        return final_results[:top_k]
    
    def _calculate_keyword_scores(
        self,
        query: str,
        results: List[RetrievalResult],
        boost_keywords: List[str] = None
    ) -> Dict[int, float]:
        """计算关键词匹配分数"""
        scores = {}
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        boost_keywords = boost_keywords or []
        boost_set = set(k.lower() for k in boost_keywords)
        
        for i, result in enumerate(results):
            content_lower = result.content.lower()
            content_words = set(re.findall(r'\w+', content_lower))
            
            # 计算词重叠率
            overlap = len(query_words & content_words)
            overlap_ratio = overlap / max(len(query_words), 1)
            
            # 加权词加成
            boost_score = sum(1 for word in boost_set if word in content_lower)
            boost_ratio = boost_score / max(len(boost_set), 1) if boost_set else 0
            
            # 综合分数
            scores[i] = 0.7 * overlap_ratio + 0.3 * boost_ratio
        
        return scores
    
    def _calculate_time_scores(
        self,
        results: List[RetrievalResult],
        decay_days: int = 365
    ) -> Dict[int, float]:
        """计算时间衰减分数（越新越高）"""
        scores = {}
        now = datetime.now()
        
        for i, result in enumerate(results):
            timestamp_str = result.metadata.get("timestamp", "")
            
            try:
                # 尝试解析时间戳
                if timestamp_str:
                    doc_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    days_diff = (now - doc_time).days
                    
                    # 指数衰减：score = e^(-days/decay_days)
                    import math
                    score = math.exp(-days_diff / decay_days)
                    scores[i] = score
                else:
                    # 没有时间戳，给中等分数
                    scores[i] = 0.5
            except:
                # 解析失败，给中等分数
                scores[i] = 0.5
        
        return scores
    
    def get_name(self) -> str:
        return "HybridRetriever"
