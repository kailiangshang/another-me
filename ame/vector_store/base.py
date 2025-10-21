"""
向量存储抽象基类
支持多种向量数据库实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class VectorStoreBase(ABC):
    """向量存储抽象基类"""
    
    @abstractmethod
    async def add_documents(self, documents: List[Dict]) -> bool:
        """
        添加文档到向量库
        
        Args:
            documents: 文档列表
            
        Returns:
            是否添加成功
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 5,
        **kwargs
    ) -> List[Dict]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            limit: 返回数量
            **kwargs: 其他参数
            
        Returns:
            相关文档列表
        """
        pass
    
    @abstractmethod
    async def delete_documents(self, ids: List[str]) -> bool:
        """
        删除文档
        
        Args:
            ids: 文档ID列表
            
        Returns:
            是否删除成功
        """
        pass
    
    @abstractmethod
    async def get_statistics(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """
        清空向量库
        
        Returns:
            是否清空成功
        """
        pass
