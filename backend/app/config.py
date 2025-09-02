import os
from sqlalchemy import create_engine
from pymongo import MongoClient
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL (from environment variable)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
postgres_engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.realestate


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/realestate"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

         # This ensures pydantic-settings looks for environment variables like DATABASE_URL
        env_prefix = ''
        extra='ignore'
        

settings = Settings()

postgres_engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)


# PostgreSQL engine should be created after settings are loaded
postgres_engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.realestate