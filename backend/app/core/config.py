from pydantic_settings import BaseSettings
from typing import Optional
import os
import json
from pathlib import Path


class DynamicSettings(BaseSettings):
    """支持动态配置和 .env 文件的配置类"""
    
    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # OpenAI - 可以为空，支持后续配置
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Embedding
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # Storage
    VECTOR_DB_PATH: str = "./data/vector_store"
    UPLOAD_DIR: str = "./data/uploads"
    DATA_DIR: str = "./data"
    CONFIG_FILE: str = "./data/runtime_config.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

    def load_runtime_config(self):
        """从运行时配置文件加载配置"""
        config_path = Path(self.CONFIG_FILE)
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    runtime_config = json.load(f)
                    # 更新配置
                    if 'OPENAI_API_KEY' in runtime_config:
                        self.OPENAI_API_KEY = runtime_config['OPENAI_API_KEY']
                    if 'OPENAI_BASE_URL' in runtime_config:
                        self.OPENAI_BASE_URL = runtime_config['OPENAI_BASE_URL']
                    if 'OPENAI_MODEL' in runtime_config:
                        self.OPENAI_MODEL = runtime_config['OPENAI_MODEL']
                    if 'EMBEDDING_MODEL' in runtime_config:
                        self.EMBEDDING_MODEL = runtime_config['EMBEDDING_MODEL']
            except Exception as e:
                print(f"Warning: Failed to load runtime config: {e}")
    
    def save_runtime_config(self, config_data: dict):
        """保存运行时配置到文件"""
        config_path = Path(self.CONFIG_FILE)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有配置
        existing_config = {}
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            except:
                pass
        
        # 合并配置
        existing_config.update(config_data)
        
        # 保存到文件
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        
        # 更新当前配置
        if 'OPENAI_API_KEY' in config_data:
            self.OPENAI_API_KEY = config_data['OPENAI_API_KEY']
        if 'OPENAI_BASE_URL' in config_data:
            self.OPENAI_BASE_URL = config_data['OPENAI_BASE_URL']
        if 'OPENAI_MODEL' in config_data:
            self.OPENAI_MODEL = config_data['OPENAI_MODEL']
        if 'EMBEDDING_MODEL' in config_data:
            self.EMBEDDING_MODEL = config_data['EMBEDDING_MODEL']
    
    def is_configured(self) -> bool:
        """检查 API Key 是否已配置"""
        return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY.strip())


settings = DynamicSettings()
# 启动时尝试加载运行时配置
settings.load_runtime_config()
