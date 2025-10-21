"""
AME - Another Me Engine
独立的技术模块引擎，提供数据处理、向量存储、LLM调用、RAG生成等核心功能
"""

__version__ = "0.2.0"
__author__ = "Another Me Team"

# 导出核心模块
from .data_processor.processor import DataProcessor
from .data_processor.analyzer import DataAnalyzer
from .data_processor.async_processor import AsyncDataProcessor
from .vector_store.factory import VectorStoreFactory
from .vector_store.base import VectorStoreBase
from .llm_caller.caller import LLMCaller
from .rag_generator.generator import RAGGenerator

__all__ = [
    "DataProcessor",
    "DataAnalyzer",
    "AsyncDataProcessor",
    "VectorStoreFactory",
    "VectorStoreBase",
    "LLMCaller",
    "RAGGenerator",
]
