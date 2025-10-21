import os
import json
from app.core.config import settings


class ConfigService:
    def __init__(self):
        self.config_file = os.path.join(settings.DATA_DIR, "config.json")
        os.makedirs(settings.DATA_DIR, exist_ok=True)
    
    async def update_api_config(self, api_key: str, base_url: str, model: str) -> dict:
        """更新 API 配置"""
        config = await self.load_config()
        
        config["api"] = {
            "api_key": api_key,
            "base_url": base_url,
            "model": model
        }
        
        await self.save_config(config)
        
        # 更新环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_BASE_URL"] = base_url
        os.environ["OPENAI_MODEL"] = model
        
        return config
    
    async def get_api_config(self) -> dict:
        """获取 API 配置"""
        config = await self.load_config()
        return config.get("api", {
            "api_key": settings.OPENAI_API_KEY,
            "base_url": settings.OPENAI_BASE_URL,
            "model": settings.OPENAI_MODEL
        })
    
    async def load_config(self) -> dict:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    async def save_config(self, config: dict):
        """保存配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
