"""
AME - Another Me Engine
独立的技术模块引擎，提供数据处理、向量存储、LLM调用、RAG生成等核心功能
"""

__version__ = "0.3.0"
__author__ = "Another Me Team"

# 导出核心模块
from .data_processor.processor import DataProcessor
from .data_processor.analyzer import DataAnalyzer
from .data_processor.async_processor import AsyncDataProcessor
from .data_processor.base import DataProcessorBase, ProcessedData

from .vector_store.factory import VectorStoreFactory
from .vector_store.base import VectorStoreBase

from .llm_caller.caller import LLMCaller
from .llm_caller.base import LLMCallerBase, LLMResponse

from .rag_generator.generator import RAGGenerator

from .retrieval.factory import RetrieverFactory
from .retrieval.base import RetrieverBase, RetrievalResult
from .retrieval.vector_retriever import VectorRetriever
from .retrieval.hybrid_retriever import HybridRetriever
from .retrieval.reranker import Reranker, LLMReranker, RerankerBase

__all__ = [
    # Data Processor
    "DataProcessor",
    "DataAnalyzer",
    "AsyncDataProcessor",
    "DataProcessorBase",
    "ProcessedData",
    
    # Vector Store
    "VectorStoreFactory",
    "VectorStoreBase",
    
    # LLM Caller
    "LLMCaller",
    "LLMCallerBase",
    "LLMResponse",
    
    # RAG Generator
    "RAGGenerator",
    
    # Retrieval
    "RetrieverFactory",
    "RetrieverBase",
    "RetrievalResult",
    "VectorRetriever",
    "HybridRetriever",
    "Reranker",
    "LLMReranker",
    "RerankerBase",
]
