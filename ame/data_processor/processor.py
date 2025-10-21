"""
数据处理模块
负责：文件解析、文本清洗、格式标准化
"""

import json
from typing import List, Dict
from datetime import datetime
import re


class DataProcessor:
    """数据处理器 - 独立的技术模块"""
    
    def __init__(self):
        self.supported_formats = ['.txt', '.json', '.md']
    
    async def process_file(self, file_path: str) -> List[Dict]:
        """
        输入：文件路径
        输出：标准化的文档列表
        """
        extension = file_path.split('.')[-1].lower()
        
        if extension == 'txt' or extension == 'md':
            return await self._process_text_file(file_path)
        elif extension == 'json':
            return await self._process_json_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    async def process_text(self, text: str, source: str, timestamp: str) -> Dict:
        """
        输入：文本内容、来源、时间戳
        输出：标准化的文档对象
        """
        cleaned_text = self._clean_text(text)
        
        return {
            "content": cleaned_text,
            "source": source,
            "timestamp": timestamp,
            "metadata": {
                "length": len(cleaned_text),
                "processed_at": datetime.now().isoformat()
            }
        }
    
    async def _process_text_file(self, file_path: str) -> List[Dict]:
        """处理文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按段落分割
        paragraphs = self._split_into_paragraphs(content)
        
        documents = []
        for para in paragraphs:
            if len(para.strip()) > 10:  # 过滤太短的段落
                doc = await self.process_text(
                    text=para,
                    source=file_path,
                    timestamp=datetime.now().isoformat()
                )
                documents.append(doc)
        
        return documents
    
    async def _process_json_file(self, file_path: str) -> List[Dict]:
        """处理 JSON 文件（如微信聊天记录导出）"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        
        # 假设格式：[{"content": "...", "timestamp": "...", "sender": "..."}]
        if isinstance(data, list):
            for item in data:
                doc = await self.process_text(
                    text=item.get("content", ""),
                    source=f"{file_path}:{item.get('sender', 'unknown')}",
                    timestamp=item.get("timestamp", datetime.now().isoformat())
                )
                documents.append(doc)
        
        return documents
    
    def _clean_text(self, text: str) -> str:
        """文本清洗"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除特殊字符（保留基本标点）
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:，。！？；：""''、]', '', text)
        return text.strip()
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """分割段落"""
        # 按换行符分割
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
