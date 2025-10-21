"""
向量存储工厂
支持多种向量数据库的切换
"""

from typing import Optional
from .base import VectorStoreBase
from .store import ChromaVectorStore
from .memu_store import MemuVectorStore


class VectorStoreFactory:
    """向量存储工厂类"""
    
    @staticmethod
    def create(
        store_type: str = "chroma",
        db_path: str = "./data/vector_store",
        **kwargs
    ) -> VectorStoreBase:
        """
        创建向量存储实例
        
        Args:
            store_type: 存储类型 ('chroma' 或 'memu')
            db_path: 数据库路径
            **kwargs: 其他参数
            
        Returns:
            向量存储实例
        """
        if store_type.lower() == "memu":
            embedding_dim = kwargs.get("embedding_dim", 1536)
            return MemuVectorStore(db_path=db_path, embedding_dim=embedding_dim)
        elif store_type.lower() == "chroma":
            return ChromaVectorStore(db_path=db_path)
        else:
            raise ValueError(f"Unsupported vector store type: {store_type}")


# 默认实例（用于向后兼容）
def VectorStore(db_path: str = "./data/vector_store") -> VectorStoreBase:
    """
    创建默认向量存储实例
    优先使用 Memu，如果不可用则使用 ChromaDB
    """
    try:
        # 尝试使用 Memu
        return VectorStoreFactory.create("memu", db_path)
    except Exception:
        # 降级到 ChromaDB
        return VectorStoreFactory.create("chroma", db_path)
