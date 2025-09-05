import os
import sys
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

# Database configurations
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/realestate")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "realestate")

def test_postgresql_upload():
    """Upload sample data to PostgreSQL properties table"""
    try:
        # Create PostgreSQL engine
        engine = create_engine(POSTGRES_URL)
        
        # Sample property data for PostgreSQL
        properties_data = [
            {
                'user_id': uuid4(),
                'title': 'Beautiful Family Home',
                'property_type': 'house',
                'price': 350000.00,
                'status': 'available',
                'created_at': datetime.now()
            },
            {
                'user_id': uuid4(),
                'title': 'Modern Downtown Apartment',
                'property_type': 'apartment',
                'price': 250000.00,
                'status': 'available',
                'created_at': datetime.now()
            },
            {
                'user_id': uuid4(),
                'title': 'Commercial Office Space',
                'property_type': 'commercial',
                'price': 750000.00,
                'status': 'available',
                'created_at': datetime.now()
            }
        ]
        
        with Session(engine) as session:
            # Insert sample data
            for prop_data in properties_data:
                session.execute(
                    text("""
                        INSERT INTO properties (user_id, title, property_type, price, status, created_at)
                        VALUES (:user_id, :title, :property_type, :price, :status, :created_at)
                    """),
                    prop_data
                )
            session.commit()
            
            # Verify insertion
            result = session.execute(text("SELECT COUNT(*) FROM properties")).scalar()
            print(f"✅ PostgreSQL: Inserted {result} properties")
            return True
            
    except Exception as e:
        print(f"❌ PostgreSQL upload failed: {e}")
        return False

def test_mongodb_upload():
    """Upload sample data to MongoDB properties collection"""
    try:
        # Create MongoDB client
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        db = client[MONGO_DB_NAME]
        
        # Sample property details for MongoDB
        property_details = [
            {
                'sql_property_id': 1,
                'location': {
                    'address': '123 Main Street',
                    'coordinates': {'lat': 40.7128, 'lng': -74.0060},
                    'street_address': '123 Main St'
                },
                'details': {
                    'bedrooms': 4,
                    'bathrooms': 3,
                    'square_feet': 2500,
                    'year_built': 2010,
                    'lot_size': 0.5
                },
                'amenities': ['pool', 'garden', 'garage', 'central_air'],
                'media': ['photo1.jpg', 'photo2.jpg'],
                'description': 'Beautiful family home in a quiet neighborhood'
            },
            {
                'sql_property_id': 2,
                'location': {
                    'address': '456 Downtown Ave',
                    'coordinates': {'lat': 40.7580, 'lng': -73.9855},
                    'street_address': '456 Downtown Ave'
                },
                'details': {
                    'bedrooms': 2,
                    'bathrooms': 2,
                    'square_feet': 1200,
                    'year_built': 2018,
                    'lot_size': 0.1
                },
                'amenities': ['gym', 'concierge', 'rooftop', 'elevator'],
                'media': ['apt1.jpg', 'apt2.jpg'],
                'description': 'Modern apartment with city views'
            }
        ]
        
        # Insert into MongoDB
        result = db.properties.insert_many(property_details)
        
        # Verify insertion
        count = db.properties.count_documents({})
        print(f"✅ MongoDB: Inserted {count} property documents")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB upload failed: {e}")
        return False

def main():
    """Main function to test both database uploads"""
    print("🚀 Starting dual database upload test...")
    
    # Test PostgreSQL upload
    postgres_success = test_postgresql_upload()
    
    # Test MongoDB upload
    mongo_success = test_mongodb_upload()
    
    # Summary
    if postgres_success and mongo_success:
        print("🎉 Both PostgreSQL and MongoDB uploads completed successfully!")
    else:
        print("⚠️  Some uploads failed. Check the error messages above.")

if __name__ == "__main__":
    main()
