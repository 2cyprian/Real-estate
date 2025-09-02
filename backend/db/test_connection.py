from sqlalchemy import text
from db.database import engine
import os
from dotenv import load_dotenv

load_dotenv()

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print("✅ Connected to PostgreSQL! Version:", version[0])
except Exception as e:
    print("❌ Connection failed:", e)
