import os
from sqlalchemy import create_engine
from pymongo import MongoClient
from pymongo.server_api import ServerApi  # Add this import
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # PostgreSQL Configuration
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/realestate")
    
    # MongoDB Configuration
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "realestate")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"

# Initialize settings
settings = Settings()

# PostgreSQL Engine
postgres_engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# MongoDB Client
mongo_client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
mongo_db = mongo_client[settings.MONGO_DB_NAME]