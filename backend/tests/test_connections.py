import os
from sqlalchemy import create_engine, text
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_postgresql_connection():
    """Test PostgreSQL database connection"""
    try:
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/realestate")
        
        # Create engine and test connection
        engine = create_engine(database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ PostgreSQL connection successful")
            print(f"   Database version: {version}")
            return True
            
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection with Server API"""
    try:
        # Get MongoDB URI from environment
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        
        # Create a new client and connect to the server with Server API
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        print("   Pinged your deployment. You successfully connected to MongoDB!")
        
        # Test database access
        db = client.realestate
        collections = db.list_collection_names()
        print(f"   Available collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def test_all_connections():
    """Test all database connections"""
    print("🔍 Testing all database connections...")
    print("=" * 50)
    
    # Test PostgreSQL
    postgres_success = test_postgresql_connection()
    print()
    
    # Test MongoDB
    mongo_success = test_mongodb_connection()
    print()
    
    # Summary
    print("=" * 50)
    if postgres_success and mongo_success:
        print("🎉 All database connections successful!")
        return True
    else:
        print("⚠️  Some connections failed. Please check your configuration.")
        return False

if __name__ == "__main__":
    test_all_connections()