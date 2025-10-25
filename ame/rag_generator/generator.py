"""
RAG 生成模块
负责:检索增强生成
"""

from typing import List, Dict, Optional, AsyncIterator
import logging
from ame.llm_caller.caller import LLMCaller
from ame.rag.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class RAGGenerator:
    """
    RAG 生成器 - 独立的技术模块
    
    结合知识检索和LLM生成，为查询提供基于知识库的答案
    """
    
    def __init__(
        self, 
        knowledge_base: KnowledgeBase,
        llm_caller: LLMCaller,
        default_top_k: int = 5,
        max_context_length: int = 3000
    ):
        """
        初始化RAG生成器
        
        Args:
            knowledge_base: 知识库实例
            llm_caller: LLM调用器实例
            default_top_k: 默认检索数量
            max_context_length: 最大上下文长度
        """
        self.knowledge_base = knowledge_base
        self.llm_caller = llm_caller
        self.default_top_k = default_top_k
        self.max_context_length = max_context_length
    
    def _build_context(self, documents: List[Dict], max_length: int) -> str:
        """构建上下文"""
        context_parts = []
        current_length = 0
        
        for doc in documents:
            content = doc.get("content", "")
            timestamp = doc.get("timestamp", "")
            
            # 格式化文档
            doc_text = f"[{timestamp}] {content}"
            doc_length = len(doc_text)
            
            if current_length + doc_length > max_length:
                break
            
            context_parts.append(doc_text)
            current_length += doc_length
        
        return "\n\n".join(context_parts)
    
    async def generate_stream(
        self,
        query: str,
        top_k: Optional[int] = None,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """
        流式生成回答
        
        Args:
            query: 查询问题
            top_k: 检索文档数量
            temperature: LLM温度参数
            
        Yields:
            生成的文本片段
        """
        if top_k is None:
            top_k = self.default_top_k
        
        # 1. 检索相关文档
        documents = await self.knowledge_base.search(
            query=query,
            top_k=top_k
        )
        
        logger.info(f"Retrieved {len(documents)} documents for streaming query")
        
        # 2. 构建上下文
        context = self._build_context(documents, self.max_context_length)
        
        # 3. 构建提示
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(query, context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # 4. 流式生成
        async for chunk in self.llm_caller.generate_stream(
            messages=messages,
            temperature=temperature
        ):
            yield chunk
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是一个基于知识库的智能助手。你的任务是根据提供的知识库内容回答用户问题。

重要原则：
1. 仅基于提供的知识库内容回答，不要编造信息
2. 如果知识库中没有相关信息，请直接说明“知识库中没有相关内容”
3. 回答要准确、简洁、有帮助
4. 如果需要，可以引用知识库中的原文
5. 保持专业、友好的语气"""
    
    def _build_user_prompt(self, query: str, context: str) -> str:
        """构建用户提示词"""
        if context:
            return f"""知识库内容：

{context}

---

问题：{query}

请基于上述知识库内容回答问题。"""
        else:
            return f"""问题：{query}

很抱歉，知识库中没有找到与这个问题相关的内容。请尝试：
1. 添加更多相关文档到知识库
2. 使用不同的关键词重新提问
3. 简化问题表达"""
    
    def _calculate_confidence(self, documents: List[Dict]) -> float:
        """计算置信度"""
        if not documents:
            return 0.0
        
        # 简单实现：基于文档数量和相似度
        # 实际项目可以使用更复杂的算法
        
        # 如果有相似度信息
        if documents and "similarity" in documents[0]:
            avg_similarity = sum(doc.get("similarity", 0) for doc in documents) / len(documents)
            return avg_similarity
        
        # 否则基于文档数量
        if len(documents) >= 5:
            return 0.8
        elif len(documents) >= 3:
            return 0.6
        elif len(documents) >= 1:
            return 0.4
        else:
            return 0.0
