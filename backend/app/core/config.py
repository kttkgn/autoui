from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 基础配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "UI自动化测试平台"
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # 数据库配置
    DATABASE_URL: str = "mysql+asyncmy://root:RootQwe123@localhost/db"
    SQLALCHEMY_DATABASE_URI: str = "mysql+pymysql://root:password@localhost:3306/uiauto"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RabbitMQ配置
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    
    # MinIO配置
    MINIO_URL: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 