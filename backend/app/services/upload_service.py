from typing import List
from fastapi import UploadFile
import aiofiles
import os
from datetime import datetime
from app.core.config import settings
from ame.data_processor.processor import DataProcessor
from ame.vector_store.store import VectorStore


class UploadService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
        self.data_processor = DataProcessor()
        self.vector_store = VectorStore()
    
    async def process_uploads(self, files: List[UploadFile]) -> List[dict]:
        """处理上传的文件"""
        results = []
        
        for file in files:
            # 保存文件
            file_path = os.path.join(self.upload_dir, file.filename)
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # 处理文件内容
            processed_data = await self.data_processor.process_file(file_path)
            
            # 向量化并存储
            await self.vector_store.add_documents(processed_data)
            
            results.append({
                "filename": file.filename,
                "size": len(content),
                "processed": len(processed_data),
                "timestamp": datetime.now().isoformat()
            })
        
        return results
    
    async def process_text(self, text: str, source: str, timestamp: str = None) -> dict:
        """处理文本内容"""
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        # 处理文本
        processed = await self.data_processor.process_text(text, source, timestamp)
        
        # 向量化并存储
        await self.vector_store.add_documents([processed])
        
        return {
            "processed": True,
            "timestamp": timestamp,
            "source": source
        }
    
    async def get_statistics(self) -> dict:
        """获取数据统计"""
        stats = await self.vector_store.get_statistics()
        return {
            "total_documents": stats.get("count", 0),
            "last_updated": stats.get("last_updated"),
            "sources": stats.get("sources", {})
        }
