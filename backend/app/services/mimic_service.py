from ame.vector_store.store import VectorStore
from ame.llm_caller.caller import LLMCaller
from ame.rag_generator.generator import RAGGenerator


class MimicService:
    """业务功能 1: 模仿我说话"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_caller = LLMCaller()
        self.rag_generator = RAGGenerator()
    
    async def generate_response(self, prompt: str, context: str = "", temperature: float = 0.7) -> dict:
        """生成模仿用户风格的回复"""
        
        # 1. 检索相关记忆
        relevant_docs = await self.vector_store.search(
            query=prompt,
            limit=5,
            filter_context=context
        )
        
        # 2. 使用 RAG 生成回复
        response = await self.rag_generator.generate(
            query=prompt,
            documents=relevant_docs,
            system_prompt=self._build_mimic_prompt(),
            temperature=temperature
        )
        
        return {
            "text": response["text"],
            "references": relevant_docs,
            "confidence": response.get("confidence", 0.0)
        }
    
    async def generate_social_post(self, topic: str, context: str = "") -> str:
        """生成社交媒体帖子"""
        
        # 检索相关的历史发言
        relevant_docs = await self.vector_store.search(
            query=topic,
            limit=3,
            filter_by_source=["social", "diary"]
        )
        
        # 构建专门的社交媒体提示词
        system_prompt = """你是用户的 AI 分身。根据用户的历史发言风格，生成一条朋友圈/社交媒体帖子。

要求：
1. 语气、风格要完全模仿用户
2. 长度控制在 50-150 字
3. 可以使用 emoji，但不要过度
4. 自然、真实，像用户自己写的

参考用户的历史发言风格。"""
        
        response = await self.rag_generator.generate(
            query=f"写一条关于「{topic}」的朋友圈",
            documents=relevant_docs,
            system_prompt=system_prompt,
            temperature=0.8
        )
        
        return response["text"]
    
    def _build_mimic_prompt(self) -> str:
        """构建模仿提示词"""
        return """你是用户的 AI 分身，你的任务是完全模仿用户的说话风格、思维方式和语气。

基于用户提供的历史对话记录、日记等数据，你需要：
1. 使用用户习惯的表达方式和词汇
2. 保持用户的语气（正式/随意、幽默/严肃等）
3. 反映用户的价值观和思考模式
4. 如果不确定，可以参考相似情境下用户的历史回复

记住：你不是助手，你是"另一个他/她"。"""
