from ame.vector_store.store import VectorStore
from ame.llm_caller.caller import LLMCaller
from ame.rag_generator.generator import RAGGenerator
from typing import Optional
from datetime import datetime
import re


class MemoryService:
    """业务功能 3: 记忆回溯对话"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_caller = LLMCaller()
        self.rag_generator = RAGGenerator()
    
    async def recall(self, query: str, time_context: Optional[str] = None, limit: int = 5) -> dict:
        """回溯记忆"""
        
        # 1. 解析时间上下文
        time_filter = None
        if time_context:
            time_filter = self._parse_time_context(time_context)
        
        # 2. 检索相关记忆
        memories = await self.vector_store.search(
            query=query,
            limit=limit,
            time_filter=time_filter
        )
        
        # 3. 使用 LLM 生成总结
        summary = await self._generate_memory_summary(query, memories, time_context)
        
        return {
            "items": memories,
            "summary": summary,
            "time_context": time_context
        }
    
    async def get_timeline(self, year: Optional[int] = None, month: Optional[int] = None) -> dict:
        """获取时间线"""
        
        # 构建时间过滤器
        if year and month:
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"
        elif year:
            start_date = f"{year}-01-01"
            end_date = f"{year+1}-01-01"
        else:
            # 默认返回最近一年
            now = datetime.now()
            start_date = f"{now.year-1}-{now.month:02d}-01"
            end_date = now.strftime("%Y-%m-%d")
        
        # 获取时间范围内的所有文档
        documents = await self.vector_store.get_documents_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        
        # 按日期分组
        timeline = {}
        for doc in documents:
            date = doc.get("timestamp", "")[:10]  # YYYY-MM-DD
            if date not in timeline:
                timeline[date] = []
            timeline[date].append(doc)
        
        return {
            "period": f"{start_date} to {end_date}",
            "timeline": timeline,
            "total": len(documents)
        }
    
    async def find_similar(self, query: str, limit: int = 5) -> list:
        """查找相似的历史时刻"""
        
        # 使用向量相似度搜索
        similar = await self.vector_store.search(
            query=query,
            limit=limit,
            include_similarity=True
        )
        
        return similar
    
    def _parse_time_context(self, time_context: str) -> dict:
        """解析时间上下文"""
        
        # 处理相对时间表达
        if "去年" in time_context or "last year" in time_context.lower():
            year = datetime.now().year - 1
            return {"year": year}
        
        if "这个时候" in time_context or "this time" in time_context.lower():
            now = datetime.now()
            return {"month": now.month, "day_range": 7}  # 前后7天
        
        # 处理绝对时间：YYYY-MM 或 YYYY
        match = re.match(r"(\d{4})(?:-(\d{2}))?", time_context)
        if match:
            year = int(match.group(1))
            month = int(match.group(2)) if match.group(2) else None
            return {"year": year, "month": month}
        
        return {}
    
    async def _generate_memory_summary(self, query: str, memories: list, time_context: Optional[str]) -> str:
        """生成记忆总结"""
        
        if not memories:
            return "没有找到相关记忆。"
        
        context = "\n\n".join([
            f"[{m.get('timestamp', 'Unknown')}] {m.get('content', '')[:200]}"
            for m in memories[:3]
        ])
        
        time_desc = f"在{time_context}，" if time_context else ""
        
        prompt = f"""基于以下记忆片段，回答用户的问题："{query}"

{time_desc}相关记忆：
{context}

请用第一人称（"我"）总结这些记忆，自然、亲切，像是在回忆往事。控制在 100-150 字。"""
        
        response = await self.llm_caller.generate(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response["content"]
