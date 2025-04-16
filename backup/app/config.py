from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "RiderCritic API"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Firebase Configuration
    firebase_project_id: str
    firebase_api_key: str
    firebase_auth_domain: str
    firebase_storage_bucket: str
    
    # CORS Settings
    allowed_origins: list = [
        "https://ridercritic.firebaseapp.com",
        "https://ridercritic.web.app",
        "http://localhost:3000",
    ]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 