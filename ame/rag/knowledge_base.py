"""
知识库管理 - RAG 核心
负责文档的向量化存储和检索
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ame.vector_store.factory import VectorStoreFactory
from ame.data_processor.processor import DataProcessor
from ame.retrieval.factory import RetrieverFactory


class KnowledgeBase:
    """知识库管理类"""
    
    def __init__(
        self,
        vector_store_type: str = "memu",
        db_path: str = "./data/rag_vector_store"
    ):
        """
        初始化知识库
        
        Args:
            vector_store_type: 向量存储类型
            db_path: 数据库路径
        """
        self.vector_store = VectorStoreFactory.create(
            store_type=vector_store_type,
            db_path=db_path
        )
        self.data_processor = DataProcessor()
        
        # 创建混合检索器
        self.retriever = RetrieverFactory.create_retriever(
            retriever_type="hybrid",
            vector_store=self.vector_store,
            vector_weight=0.6,
            keyword_weight=0.3,
            time_weight=0.1
        )
    
    async def add_document(
        self,
        file_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        添加文档到知识库
        
        Args:
            file_path: 文件路径
            metadata: 元数据
            
        Returns:
            处理结果
        """
        # 处理文件
        processed_data = await self.data_processor.process_file(file_path)
        
        # 添加自定义元数据
        if metadata:
            for item in processed_data:
                item['metadata'].update(metadata)
        
        # 存储到向量库
        await self.vector_store.add_documents(processed_data)
        
        return {
            "success": True,
            "file": Path(file_path).name,
            "documents_count": len(processed_data)
        }
    
    async def add_text(
        self,
        text: str,
        source: str = "user_input",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        添加文本到知识库
        
        Args:
            text: 文本内容
            source: 来源
            metadata: 元数据
            
        Returns:
            处理结果
        """
        processed = await self.data_processor.process_text(
            text=text,
            source=source
        )
        
        if metadata:
            processed['metadata'].update(metadata)
        
        await self.vector_store.add_documents([processed])
        
        return {
            "success": True,
            "source": source
        }
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        检索知识库
        
        Args:
            query: 查询文本
            top_k: 返回数量
            filters: 过滤条件
            
        Returns:
            检索结果
        """
        results = await self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters
        )
        
        return [r.to_dict() for r in results]
    
    async def get_statistics(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        stats = await self.vector_store.get_statistics()
        return {
            "total_documents": stats.get("count", 0),
            "last_updated": stats.get("last_updated"),
            "sources": stats.get("sources", {})
        }
