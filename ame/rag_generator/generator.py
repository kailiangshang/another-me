"""
RAG 生成模块
负责：检索增强生成
"""

from typing import List, Dict, Optional
from ame.llm_caller.caller import LLMCaller


class RAGGenerator:
    """RAG 生成器 - 独立的技术模块"""
    
    def __init__(self):
        self.llm_caller = LLMCaller()
    
    async def generate(
        self,
        query: str,
        documents: List[Dict],
        system_prompt: str,
        temperature: float = 0.7,
        max_context_length: int = 2000
    ) -> Dict:
        """
        输入：查询、检索文档、系统提示、温度
        输出：生成结果（包含文本和置信度）
        """
        # 1. 构建上下文
        context = self._build_context(documents, max_context_length)
        
        # 2. 构建完整提示
        full_prompt = self._build_prompt(query, context)
        
        # 3. 调用 LLM 生成
        response = await self.llm_caller.generate_with_system(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=temperature
        )
        
        # 4. 计算置信度（基于检索文档的相关性）
        confidence = self._calculate_confidence(documents)
        
        return {
            "text": response["content"],
            "confidence": confidence,
            "context_used": len(documents),
            "usage": response.get("usage", {})
        }
    
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
    
    def _build_prompt(self, query: str, context: str) -> str:
        """构建提示"""
        if context:
            return f"""参考以下历史记录：

{context}

---

基于以上信息，{query}"""
        else:
            return query
    
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
