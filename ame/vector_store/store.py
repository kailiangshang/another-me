"""
向量存储模块 (使用 ChromaDB 作为 Memu 的替代，因为 Memu 不是标准库)
负责：文档向量化、存储、检索
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings as app_settings
from .base import VectorStoreBase


class ChromaVectorStore(VectorStoreBase):
    """ChromaDB 向量存储实现"""
    
    def __init__(self):
        # 初始化 ChromaDB (可替换为 Memu)
        self.client = chromadb.PersistentClient(
            path=app_settings.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="another_me_memories",
            metadata={"description": "用户记忆向量库"}
        )
    
    async def add_documents(self, documents: List[Dict]) -> bool:
        """添加文档到向量库"""
        if not documents:
            return False
        
        # 准备数据
        ids = [f"doc_{datetime.now().timestamp()}_{i}" for i in range(len(documents))]
        texts = [doc.get("content", "") for doc in documents]
        metadatas = [
            {
                "source": doc.get("source", "unknown"),
                "timestamp": doc.get("timestamp", datetime.now().isoformat()),
                **doc.get("metadata", {})
            }
            for doc in documents
        ]
        
        # 添加到向量库
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        return True
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        filter_context: Optional[str] = None,
        filter_by_source: Optional[List[str]] = None,
        time_filter: Optional[Dict] = None,
        include_similarity: bool = False,
        **kwargs
    ) -> List[Dict]:
        """语义搜索"""
        # 构建过滤条件
        where = {}
        if filter_by_source:
            where["source"] = {"$in": filter_by_source}
        
        # TODO: 添加时间过滤逻辑
        
        # 执行查询
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where if where else None
        )
        
        # 格式化结果
        documents = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                doc_dict = {
                    "content": doc,
                    "source": metadata.get("source", "unknown"),
                    "timestamp": metadata.get("timestamp", ""),
                    "metadata": metadata
                }
                
                if include_similarity and results["distances"]:
                    doc_dict["similarity"] = 1 - results["distances"][0][i]  # 转换距离为相似度
                
                documents.append(doc_dict)
        
        return documents
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """删除文档"""
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
    
    async def clear(self) -> bool:
        """清空向量库"""
        try:
            self.client.delete_collection(name="another_me_memories")
            self.collection = self.client.get_or_create_collection(
                name="another_me_memories",
                metadata={"description": "用户记忆向量库"}
            )
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    
    async def get_documents_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """获取时间范围内的文档"""
        # 获取所有文档（简化实现，实际应使用过滤）
        all_docs = self.collection.get()
        
        documents = []
        for i, doc in enumerate(all_docs["documents"]):
            metadata = all_docs["metadatas"][i] if all_docs["metadatas"] else {}
            timestamp = metadata.get("timestamp", "")
            
            # 时间过滤
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            
            documents.append({
                "content": doc,
                "source": metadata.get("source", "unknown"),
                "timestamp": timestamp,
                "metadata": metadata
            })
        
        return documents
    
    async def get_all_documents(self) -> List[Dict]:
        """获取所有文档"""
        all_docs = self.collection.get()
        
        documents = []
        for i, doc in enumerate(all_docs["documents"]):
            metadata = all_docs["metadatas"][i] if all_docs["metadatas"] else {}
            documents.append({
                "content": doc,
                "source": metadata.get("source", "unknown"),
                "timestamp": metadata.get("timestamp", ""),
                "metadata": metadata
            })
        
        return documents
    
    async def get_statistics(self) -> Dict:
        """获取统计信息"""
        count = self.collection.count()
        
        # 获取来源统计
        all_docs = self.collection.get()
        sources = {}
        for metadata in all_docs["metadatas"]:
            source = metadata.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "count": count,
            "sources": sources,
            "last_updated": datetime.now().isoformat()
        }
