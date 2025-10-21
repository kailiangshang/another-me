"""
数据处理器抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessedData:
    """处理后的数据"""
    content: str
    source: str
    timestamp: str
    metadata: Dict[str, Any]
    data_type: str  # text, image, audio, etc.
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "data_type": self.data_type
        }


class DataProcessorBase(ABC):
    """数据处理器抽象基类"""
    
    @abstractmethod
    async def process_file(self, file_path: str, **kwargs) -> List[ProcessedData]:
        """
        处理文件
        
        Args:
            file_path: 文件路径
            **kwargs: 其他参数
            
        Returns:
            处理后的数据列表
        """
        pass
    
    @abstractmethod
    async def process_text(
        self,
        text: str,
        source: str = "user_input",
        timestamp: Optional[str] = None,
        **kwargs
    ) -> ProcessedData:
        """
        处理文本
        
        Args:
            text: 文本内容
            source: 数据来源
            timestamp: 时间戳
            **kwargs: 其他参数
            
        Returns:
            处理后的数据
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        获取支持的文件格式
        
        Returns:
            格式列表，如 ['txt', 'md', 'json']
        """
        pass
    
    def _get_timestamp(self, custom_timestamp: Optional[str] = None) -> str:
        """获取时间戳"""
        if custom_timestamp:
            return custom_timestamp
        return datetime.now().isoformat()
