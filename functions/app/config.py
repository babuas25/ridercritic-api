from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Application settings
    app_name: str = "RiderCritic"
    version: str = "1.0.0"
    debug: bool = False
    
    # Firebase settings
    firebase_project_id: str
    firebase_api_key: str
    firebase_auth_domain: str
    firebase_storage_bucket: str
    
    # CORS settings
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 