"""
Memu 向量存储实现
高性能的向量检索库
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
import logging
from .base import VectorStoreBase

logger = logging.getLogger(__name__)


class MemuVectorStore(VectorStoreBase):
    """
    Memu 向量存储实现
    
    注意: Memu 是一个轻量级的向量检索库
    这里提供一个简化的实现，实际使用时需要安装 memu 库
    """
    
    def __init__(self, db_path: str, embedding_dim: int = 1536, use_openai_embedding: bool = False):
        """
        初始化 Memu 向量存储
        
        Args:
            db_path: 数据库路径
            embedding_dim: 向量维度
            use_openai_embedding: 是否使用OpenAI Embedding API
        """
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.use_openai_embedding = use_openai_embedding
        os.makedirs(db_path, exist_ok=True)
        
        # 数据存储文件
        self.data_file = os.path.join(db_path, "documents.json")
        self.index_file = os.path.join(db_path, "index.npy")
        
        # 加载或初始化数据
        self._load_data()
        
        # OpenAI客户端（延迟初始化）
        self._openai_client = None
    
    def _load_data(self) -> None:
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                logger.info(f"Loaded {len(self.documents)} documents")
            except Exception as e:
                logger.error(f"Failed to load documents: {e}")
                self.documents = []
        else:
            self.documents = []
        
        if os.path.exists(self.index_file):
            try:
                self.embeddings = np.load(self.index_file)
                logger.info(f"Loaded {len(self.embeddings)} embeddings")
            except Exception as e:
                logger.error(f"Failed to load embeddings: {e}")
                self.embeddings = np.array([]).reshape(0, self.embedding_dim)
        else:
            self.embeddings = np.array([]).reshape(0, self.embedding_dim)
    
    def _save_data(self) -> None:
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            if len(self.embeddings) > 0:
                np.save(self.index_file, self.embeddings)
            
            logger.debug(f"Saved {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            raise
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        生成文本向量
        
        Args:
            text: 输入文本
            
        Returns:
            文本向量
        """
        if self.use_openai_embedding:
            return self._generate_openai_embedding(text)
        else:
            return self._generate_hash_embedding(text)
    
    def _generate_openai_embedding(self, text: str) -> np.ndarray:
        """使用OpenAI API生成嵌入向量"""
        if self._openai_client is None:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                return self._generate_hash_embedding(text)
        
        try:
            response = self._openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            return embedding
        except Exception as e:
            logger.warning(f"OpenAI embedding failed, using hash: {e}")
            return self._generate_hash_embedding(text)
    
    def _generate_hash_embedding(self, text: str) -> np.ndarray:
        """
        使用哈希方法生成向量（fallback）
        
        注意: 这是一个简单的fallback方案，仅用于测试
        生产环境应使用真实的embedding模型
        """
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # 扩展到指定维度
        vector = np.frombuffer(hash_bytes, dtype=np.uint8)
        vector = np.tile(vector, (self.embedding_dim // len(vector) + 1))[:self.embedding_dim]
        
        # 归一化
        vector = vector.astype(np.float32)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    async def add_documents(self, documents: List[Dict]) -> bool:
        """添加文档"""
        try:
            for doc in documents:
                # 生成向量
                content = doc.get("content", "")
                embedding = self._generate_embedding(content)
                
                # 添加文档
                doc_with_id = {
                    "id": f"doc_{len(self.documents)}_{datetime.now().timestamp()}",
                    **doc
                }
                self.documents.append(doc_with_id)
                
                # 添加向量
                if len(self.embeddings) == 0:
                    self.embeddings = embedding.reshape(1, -1)
                else:
                    self.embeddings = np.vstack([self.embeddings, embedding])
            
            # 保存
            self._save_data()
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        filter_context: Optional[str] = None,
        time_filter: Optional[Dict] = None,
        include_similarity: bool = False,
        **kwargs
    ) -> List[Dict]:
        """语义搜索"""
        if len(self.documents) == 0:
            return []
        
        # 生成查询向量
        query_embedding = self._generate_embedding(query)
        
        # 计算余弦相似度
        similarities = np.dot(self.embeddings, query_embedding)
        
        # 获取 top-k
        top_indices = np.argsort(similarities)[::-1][:limit]
        
        # 构建结果
        results = []
        for idx in top_indices:
            doc = self.documents[idx].copy()
            if include_similarity:
                doc["similarity"] = float(similarities[idx])
            results.append(doc)
        
        return results
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """删除文档"""
        try:
            indices_to_delete = []
            for i, doc in enumerate(self.documents):
                if doc.get("id") in ids:
                    indices_to_delete.append(i)
            
            # 删除文档和向量
            for idx in sorted(indices_to_delete, reverse=True):
                del self.documents[idx]
                self.embeddings = np.delete(self.embeddings, idx, axis=0)
            
            self._save_data()
            return True
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
    
    async def get_documents_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """获取时间范围内的文档"""
        results = []
        for doc in self.documents:
            timestamp = doc.get("timestamp", "")
            
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            
            results.append(doc)
        
        return results
    
    async def get_all_documents(self) -> List[Dict]:
        """获取所有文档"""
        return self.documents.copy()
    
    async def get_statistics(self) -> Dict:
        """获取统计信息"""
        sources = {}
        for doc in self.documents:
            source = doc.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "count": len(self.documents),
            "sources": sources,
            "last_updated": datetime.now().isoformat(),
            "embedding_dim": self.embedding_dim
        }
    
    async def clear(self) -> bool:
        """清空向量库"""
        try:
            self.documents = []
            self.embeddings = np.array([]).reshape(0, self.embedding_dim)
            self._save_data()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
