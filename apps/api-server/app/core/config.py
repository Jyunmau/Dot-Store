"""
Dot-Store V2.1 核心配置模块
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    应用配置类
    """
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # 应用配置
    APP_NAME: str = "Dot-Store API"
    APP_VERSION: str = "2.1.0"
    APP_DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/dot_store"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30天
    
    # 密码配置
    PASSWORD_BCRYPT_ROUNDS: int = 12
    PASSWORD_MIN_LENGTH: int = 8
    
    # 登录安全配置
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 30
    
    # CORS配置
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例（单例模式）
    """
    return Settings()


settings = get_settings()
