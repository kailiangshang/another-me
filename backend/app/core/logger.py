"""
日志配置模块
提供统一的日志管理
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(
    name: str = "another_me",
    log_dir: str = "./logs",
    level: int = logging.INFO
) -> logging.Logger:
    """
    配置日志记录器
    
    Args:
        name: 日志记录器名称
        log_dir: 日志目录
        level: 日志级别
        
    Returns:
        配置好的日志记录器
    """
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（按日期）
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, f"another_me_{today}.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=30,  # 保留30天
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 错误日志单独文件
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, f"errors_{today}.log"),
        maxBytes=10*1024*1024,
        backupCount=90,  # 错误日志保留90天
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger


# 全局日志记录器
logger = setup_logger()


def get_logger(name: str = None) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 模块名称
        
    Returns:
        日志记录器
    """
    if name:
        return logging.getLogger(f"another_me.{name}")
    return logger
