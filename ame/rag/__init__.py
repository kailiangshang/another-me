"""
RAG (Retrieval-Augmented Generation) 模块
用于知识库管理、文档上传、知识检索
"""

from .knowledge_base import KnowledgeBase
from .document_manager import DocumentManager
from .qa_engine import QAEngine

__all__ = [
    'KnowledgeBase',
    'DocumentManager',
    'QAEngine',
]
