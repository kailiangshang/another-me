"""
模仿引擎 - 学习和模仿用户说话风格
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ame.llm_caller.caller import LLMCaller
from ame.vector_store.factory import VectorStoreFactory
from ame.retrieval.factory import RetrieverFactory


class MimicEngine:
    """模仿引擎 - 让 AI 用你的方式说话"""
    
    def __init__(
        self,
        llm_caller: LLMCaller,
        vector_store_type: str = "memu",
        db_path: str = "./data/mem_vector_store"
    ):
        """
        初始化模仿引擎
        
        Args:
            llm_caller: LLM 调用器
            vector_store_type: 向量存储类型
            db_path: 数据库路径
        """
        self.llm_caller = llm_caller
        
        # 创建用户对话记录的向量存储
        self.vector_store = VectorStoreFactory.create(
            store_type=vector_store_type,
            db_path=db_path
        )
        
        # 创建检索器（更注重时间和关键词）
        self.retriever = RetrieverFactory.create_retriever(
            retriever_type="hybrid",
            vector_store=self.vector_store,
            vector_weight=0.4,
            keyword_weight=0.4,
            time_weight=0.2
        )
    
    async def learn_from_conversation(
        self,
        user_message: str,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        从用户对话中学习
        
        Args:
            user_message: 用户消息
            context: 对话上下文
            metadata: 元数据
        """
        from datetime import datetime
        
        # 构建学习数据
        doc = {
            "content": user_message,
            "source": "user_conversation",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "context": context or "",
                **(metadata or {})
            }
        }
        
        # 存储到记忆库
        await self.vector_store.add_documents([doc])
    
    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.8,
        use_history: bool = True
    ) -> str:
        """
        生成模仿用户风格的回复
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            use_history: 是否使用历史记录
            
        Returns:
            生成的回复
        """
        # 检索相关的历史对话
        relevant_history = []
        if use_history:
            results = await self.retriever.retrieve(
                query=prompt,
                top_k=5
            )
            relevant_history = [r.to_dict() for r in results]
        
        # 构建系统提示词
        system_prompt = self._build_mimic_prompt(relevant_history)
        
        # 生成回复
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_caller.generate(
            messages=messages,
            temperature=temperature
        )
        
        return response.content
    
    async def generate_response_stream(
        self,
        prompt: str,
        temperature: float = 0.8,
        use_history: bool = True
    ) -> AsyncIterator[str]:
        """
        流式生成模仿用户风格的回复
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            use_history: 是否使用历史记录
            
        Yields:
            生成的文本片段
        """
        # 检索相关的历史对话
        relevant_history = []
        if use_history:
            results = await self.retriever.retrieve(
                query=prompt,
                top_k=5
            )
            relevant_history = [r.to_dict() for r in results]
        
        # 构建系统提示词
        system_prompt = self._build_mimic_prompt(relevant_history)
        
        # 流式生成回复
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        async for chunk in self.llm_caller.generate_stream(
            messages=messages,
            temperature=temperature
        ):
            yield chunk
    
    def _build_mimic_prompt(self, history: List[Dict]) -> str:
        """构建模仿提示词"""
        
        if not history:
            return """你是用户的 AI 分身。虽然没有足够的历史数据，但请尽量保持自然、真实的对话风格。

请记住：
1. 你不是助手，你是"另一个他/她"
2. 用第一人称"我"来回答
3. 保持自然、真诚的语气
4. 不要过于正式或过于随意"""
        
        # 提取历史对话示例
        examples = "\n".join([
            f"- {h['content'][:100]}..."
            for h in history[:3]
        ])
        
        return f"""你是用户的 AI 分身，你的任务是完全模仿用户的说话风格、思维方式和语气。

基于用户的历史对话记录，你需要：
1. 使用用户习惯的表达方式和词汇
2. 保持用户的语气（正式/随意、幽默/严肃等）
3. 反映用户的价值观和思考模式
4. 用第一人称"我"来回答

参考用户的历史发言：
{examples}

记住：你不是助手，你是"另一个他/她"。"""
