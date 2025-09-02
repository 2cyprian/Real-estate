from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Update this with your actual database URL from .env
SQLALCHEMY_DATABASE_URL =os.getenv( "DATABASE_URL","postgresql+psycopg2://user:password@localhost/dbname")

engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True,future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()