"""
重排序器 - 对检索结果进行重新排序
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .base import RetrievalResult
import re


class RerankerBase(ABC):
    """重排序器抽象基类"""
    
    @abstractmethod
    async def rerank(
        self,
        query: str,
        results: List[RetrievalResult],
        top_k: int = None
    ) -> List[RetrievalResult]:
        """
        重新排序检索结果
        
        Args:
            query: 原始查询
            results: 检索结果
            top_k: 返回前k个结果
            
        Returns:
            重排序后的结果
        """
        pass


class Reranker(RerankerBase):
    """基于规则的重排序器"""
    
    def __init__(self, strategy: str = "diversity"):
        """
        初始化重排序器
        
        Args:
            strategy: 重排序策略
                - diversity: 多样性优先
                - relevance: 相关性优先
                - recency: 时效性优先
        """
        self.strategy = strategy
    
    async def rerank(
        self,
        query: str,
        results: List[RetrievalResult],
        top_k: int = None
    ) -> List[RetrievalResult]:
        """重排序"""
        if not results:
            return results
        
        if self.strategy == "diversity":
            reranked = await self._diversity_rerank(results)
        elif self.strategy == "recency":
            reranked = await self._recency_rerank(results)
        else:  # relevance
            reranked = results  # 保持原有排序
        
        if top_k:
            return reranked[:top_k]
        return reranked
    
    async def _diversity_rerank(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """
        多样性重排序：避免内容重复
        使用 MMR (Maximal Marginal Relevance) 策略
        """
        if len(results) <= 1:
            return results
        
        selected = [results[0]]  # 选择第一个（最相关的）
        remaining = results[1:]
        
        lambda_param = 0.7  # 相关性权重
        
        while remaining and len(selected) < len(results):
            max_mmr = -float('inf')
            max_idx = 0
            
            for i, candidate in enumerate(remaining):
                # 计算与查询的相关性
                relevance = candidate.score
                
                # 计算与已选择文档的最大相似度
                max_sim = 0
                for selected_doc in selected:
                    sim = self._calculate_similarity(candidate, selected_doc)
                    max_sim = max(max_sim, sim)
                
                # MMR 分数
                mmr = lambda_param * relevance - (1 - lambda_param) * max_sim
                
                if mmr > max_mmr:
                    max_mmr = mmr
                    max_idx = i
            
            # 选择 MMR 最高的文档
            selected.append(remaining.pop(max_idx))
        
        return selected
    
    async def _recency_rerank(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """时效性重排序：优先返回最新的文档"""
        from datetime import datetime
        
        def get_time_score(result: RetrievalResult) -> float:
            timestamp_str = result.metadata.get("timestamp", "")
            try:
                if timestamp_str:
                    doc_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    return doc_time.timestamp()
                return 0
            except:
                return 0
        
        # 按时间戳排序（最新的在前）
        sorted_results = sorted(results, key=get_time_score, reverse=True)
        return sorted_results
    
    def _calculate_similarity(self, doc1: RetrievalResult, doc2: RetrievalResult) -> float:
        """
        计算两个文档的相似度（简化版：基于词重叠）
        """
        words1 = set(re.findall(r'\w+', doc1.content.lower()))
        words2 = set(re.findall(r'\w+', doc2.content.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0


class LLMReranker(RerankerBase):
    """基于 LLM 的重排序器（高级功能）"""
    
    def __init__(self, llm_caller=None):
        """
        初始化 LLM 重排序器
        
        Args:
            llm_caller: LLM 调用器实例
        """
        self.llm_caller = llm_caller
    
    async def rerank(
        self,
        query: str,
        results: List[RetrievalResult],
        top_k: int = None
    ) -> List[RetrievalResult]:
        """
        使用 LLM 对结果进行重排序
        根据查询意图和文档相关性进行智能排序
        """
        if not self.llm_caller or not results:
            return results[:top_k] if top_k else results
        
        # 构建 LLM 提示
        prompt = self._build_rerank_prompt(query, results)
        
        try:
            # 调用 LLM 获取排序
            response = await self.llm_caller.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # 解析 LLM 返回的排序索引
            ranked_indices = self._parse_ranking(response.get("content", ""))
            
            # 根据索引重排序
            reranked = [results[i] for i in ranked_indices if i < len(results)]
            
            # 补充未排序的文档
            remaining = [r for i, r in enumerate(results) if i not in ranked_indices]
            reranked.extend(remaining)
            
            return reranked[:top_k] if top_k else reranked
        except:
            # LLM 调用失败，返回原始结果
            return results[:top_k] if top_k else results
    
    def _build_rerank_prompt(self, query: str, results: List[RetrievalResult]) -> str:
        """构建重排序提示"""
        docs_text = "\n\n".join([
            f"文档{i}: {result.content[:200]}..."
            for i, result in enumerate(results)
        ])
        
        return f"""请根据查询意图，对以下文档按相关性从高到低排序。

查询：{query}

文档列表：
{docs_text}

请只返回文档编号，用逗号分隔，例如：0,2,1,3"""
    
    def _parse_ranking(self, response: str) -> List[int]:
        """解析 LLM 返回的排序"""
        import re
        # 提取数字
        numbers = re.findall(r'\d+', response)
        return [int(n) for n in numbers]
