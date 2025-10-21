from ame.vector_store.store import VectorStore
from ame.data_processor.analyzer import DataAnalyzer
from ame.llm_caller.caller import LLMCaller
from typing import Optional


class AnalysisService:
    """业务功能 2: 自我认知分析"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.analyzer = DataAnalyzer()
        self.llm_caller = LLMCaller()
    
    async def generate_report(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        analysis_type: str = "comprehensive"
    ) -> dict:
        """生成自我认知分析报告"""
        
        # 1. 获取数据
        data = await self.vector_store.get_documents_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        
        # 2. 进行各项分析
        report = {}
        
        if analysis_type in ["comprehensive", "emotion"]:
            report["emotions"] = await self.analyze_emotions(data)
        
        if analysis_type in ["comprehensive", "keywords"]:
            report["keywords"] = await self.extract_keywords(data)
        
        if analysis_type in ["comprehensive", "relationships"]:
            report["relationships"] = await self.analyze_relationships(data)
        
        # 3. 使用 LLM 生成总结
        if analysis_type == "comprehensive":
            report["summary"] = await self._generate_summary(report)
        
        return report
    
    async def analyze_emotions(self, data=None) -> dict:
        """情绪分析"""
        if data is None:
            data = await self.vector_store.get_all_documents()
        
        emotions = await self.analyzer.analyze_emotions(data)
        
        return {
            "overall": emotions.get("overall", "neutral"),
            "distribution": emotions.get("distribution", {}),
            "trend": emotions.get("trend", []),
            "insights": emotions.get("insights", [])
        }
    
    async def extract_keywords(self, data=None) -> dict:
        """关键词提取（词云）"""
        if data is None:
            data = await self.vector_store.get_all_documents()
        
        keywords = await self.analyzer.extract_keywords(data, top_k=50)
        
        return {
            "keywords": keywords,  # [{"word": "xx", "weight": 0.9}, ...]
            "topics": await self.analyzer.extract_topics(data),
            "frequent_phrases": await self.analyzer.extract_phrases(data)
        }
    
    async def analyze_relationships(self, data=None) -> dict:
        """人际关系分析"""
        if data is None:
            data = await self.vector_store.get_all_documents()
        
        relationships = await self.analyzer.analyze_relationships(data)
        
        return {
            "people": relationships.get("people", []),  # [{"name": "xx", "frequency": 10, "sentiment": 0.8}]
            "network": relationships.get("network", {}),
            "insights": relationships.get("insights", [])
        }
    
    async def _generate_summary(self, report: dict) -> str:
        """使用 LLM 生成报告总结"""
        
        prompt = f"""基于以下自我认知分析数据，生成一份简洁、有洞察力的总结报告：

情绪分析：{report.get('emotions', {})}
关键词：{report.get('keywords', {}).get('keywords', [])[:10]}
人际关系：{report.get('relationships', {}).get('people', [])[:5]}

请生成 200-300 字的总结，包括：
1. 整体情绪状态
2. 主要关注点
3. 人际关系特点
4. 值得注意的变化或模式
"""
        
        response = await self.llm_caller.generate(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response["content"]
