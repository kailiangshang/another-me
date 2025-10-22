"""
异步数据处理器
支持并发处理大量文件
"""

import asyncio
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from .processor import DataProcessor

# 使用标准 logging
logger = logging.getLogger(__name__)


class AsyncDataProcessor:
    """异步数据处理器"""
    
    def __init__(self, max_workers: int = 4):
        """
        Args:
            max_workers: 最大并发数
        """
        self.processor = DataProcessor()
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_files_concurrent(self, file_paths: List[str]) -> List[Dict]:
        """
        并发处理多个文件
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            处理结果列表
        """
        logger.info(f"Starting concurrent processing of {len(file_paths)} files")
        
        # 创建任务
        tasks = [
            self._process_file_async(file_path)
            for file_path in file_paths
        ]
        
        # 并发执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤错误
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing file {file_paths[i]}: {str(result)}")
            else:
                valid_results.extend(result)
        
        logger.info(f"Completed processing: {len(valid_results)} documents")
        
        return valid_results
    
    async def _process_file_async(self, file_path: str) -> List[Dict]:
        """异步处理单个文件"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._process_file_sync,
            file_path
        )
    
    def _process_file_sync(self, file_path: str) -> List[Dict]:
        """同步处理文件（在线程池中执行）"""
        import asyncio
        # 创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.processor.process_file(file_path))
        finally:
            loop.close()
    
    async def process_texts_concurrent(self, texts: List[Dict]) -> List[Dict]:
        """
        并发处理多个文本
        
        Args:
            texts: 文本列表 [{"text": "...", "source": "...", "timestamp": "..."}]
            
        Returns:
            处理结果列表
        """
        logger.info(f"Starting concurrent processing of {len(texts)} texts")
        
        tasks = [
            self.processor.process_text(
                text=item["text"],
                source=item.get("source", "unknown"),
                timestamp=item.get("timestamp")
            )
            for item in texts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing text {i}: {str(result)}")
            else:
                valid_results.append(result)
        
        logger.info(f"Completed processing: {len(valid_results)} documents")
        
        return valid_results
    
    def __del__(self):
        """清理资源"""
        self.executor.shutdown(wait=False)
