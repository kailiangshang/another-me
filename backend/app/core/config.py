from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Embedding
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # Storage
    VECTOR_DB_PATH: str = "./data/vector_store"
    UPLOAD_DIR: str = "./data/uploads"
    DATA_DIR: str = "./data"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
