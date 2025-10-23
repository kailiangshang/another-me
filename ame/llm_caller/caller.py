"""
LLM 调用模块
负责：与 OpenAI Compatible API 交互
优化：重试机制、流式输出、缓存、错误处理
"""

from openai import OpenAI
import os
from typing import List, Dict, Optional, AsyncIterator
import time
import hashlib
import json
from functools import lru_cache

# 默认配置
DEFAULT_CONFIG = {
    "OPENAI_API_KEY": "",
    "OPENAI_BASE_URL": "https://api.openai.com/v1",
    "OPENAI_MODEL": "gpt-3.5-turbo"
}


class LLMCaller:
    """
    LLM 调用器 - 独立的技术模块
    
    特性：
    - 自动重试机制
    - 缓存支持
    - 流式输出
    - 错误处理
    """
    
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None, max_retries: int = 3, cache_enabled: bool = True):
        """
        初始化 LLM 调用器
        
        Args:
            api_key: OpenAI API Key
            base_url: API Base URL
            model: 默认模型
            max_retries: 最大重试次数
            cache_enabled: 是否启用缓存
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", DEFAULT_CONFIG["OPENAI_API_KEY"])
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", DEFAULT_CONFIG["OPENAI_BASE_URL"])
        self.model = model or os.getenv("OPENAI_MODEL", DEFAULT_CONFIG["OPENAI_MODEL"])
        self.client = None
        self.max_retries = max_retries
        self.cache_enabled = cache_enabled
        self._cache = {}
        self._init_client()
    
    def _init_client(self):
        """初始化 OpenAI 客户端"""
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
    
    def _get_cache_key(self, messages: List[Dict], model: str, temperature: float) -> str:
        """生成缓存键"""
        cache_data = {
            "messages": messages,
            "model": model,
            "temperature": temperature
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """从缓存获取"""
        if not self.cache_enabled:
            return None
        return self._cache.get(cache_key)
    
    def _save_to_cache(self, cache_key: str, response: Dict):
        """保存到缓存"""
        if self.cache_enabled:
            self._cache[cache_key] = response
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict:
        """
        生成文本
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度
            max_tokens: 最大 token 数
            stream: 是否使用流式输出
            
        Returns:
            生成结果
        """
        if not self.client:
            self._init_client()
        
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        if not model:
            model = self.model
        
        # 检查缓存
        cache_key = self._get_cache_key(messages, model, temperature)
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            return cached_response
        
        # 重试机制
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream
                )
                
                if stream:
                    # 流式输出（暂不缓存）
                    return {"stream": response}
                
                result = {
                    "content": response.choices[0].message.content,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
                
                # 保存到缓存
                self._save_to_cache(cache_key, result)
                
                return result
            
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # 指数退避
                    wait_time = (2 ** attempt) * 0.5
                    time.sleep(wait_time)
                    continue
        
        raise Exception(f"LLM generation failed after {self.max_retries} attempts: {str(last_error)}")
    
    async def generate_with_system(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float = 0.7
    ) -> Dict:
        """
        输入：用户提示、系统提示、温度
        输出：生成结果
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return await self.generate(messages, temperature=temperature)
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        流式生成文本
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度
            max_tokens: 最大 token 数
            
        Yields:
            生成的文本片段
        """
        if not self.client:
            self._init_client()
        
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        if not model:
            model = self.model
        
        # 重试机制
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                
                return
            
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait_time = (2 ** attempt) * 0.5
                    time.sleep(wait_time)
                    continue
        
        raise Exception(f"LLM generation failed after {self.max_retries} attempts: {str(last_error)}")
