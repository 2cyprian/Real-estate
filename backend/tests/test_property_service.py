# tests/test_property_service.py
import pytest
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool # Use NullPool for tests
from app.properties.models import Property
from app.properties.schema import PropertyCreate
from app.properties.services import PropertyService
from db.database import Base
import os
from dotenv import load_dotenv
from app.users.models import User # Import the User model

# Load .env file for DATABASE_URL
load_dotenv()

# -------------------------
# PostgreSQL Test Database Setup
# -------------------------
# Get DATABASE_URL from environment, ensure it's your test database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set for tests.")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool, # Use NullPool for testing to avoid connection issues
)

# -------------------------
# Mock MongoDB
# -------------------------
class MockMongoDB:
    def __init__(self):
        self.properties = {}

    def insert_property(self, document):
        from bson import ObjectId
        doc_id = ObjectId()
        self.properties[str(doc_id)] = document
        # Return a mock InsertResult
        return type("InsertResult", (), {"inserted_id": doc_id})()

    def get_property_by_sql_id(self, sql_id):
        return next(
            (doc for doc in self.properties.values() if doc.get("sql_property_id") == sql_id),
            None,
        )

    def update_property(self, doc_id, updates):
        if doc_id in self.properties:
            self.properties[doc_id].update(updates)
            return True
        return False

    def delete_property(self, doc_id):
        return self.properties.pop(doc_id, None) is not None

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture(scope="function")
def test_db():
    # Drop all tables and recreate them for a clean state for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine) # Clean up after test

@pytest.fixture
def mock_mongo():
    return MockMongoDB()

@pytest.fixture
def property_service(test_db, mock_mongo):
    return PropertyService(db=test_db, mongo_db=mock_mongo)

@pytest.fixture
def sample_user_id():
    return uuid4()

@pytest.fixture
def sample_property_data(sample_user_id):
    return {
        "user_id": sample_user_id,
        "title": "Beautiful Family Home",
        "property_type": "house",
        "price": 350000.0,
        "status": "available",
        "location": {
            "address": "Kariakoo Street",
            "city": "Dar es Salaam",
            "state": "DSM",
            "country": "Tanzania",
            "zip_code": "11101",
            "coordinates": {"lat": -6.7924, "lng": 39.2083}
        },
        "details": {
            "bedrooms": 4,
            "bathrooms": 2,
            "square_feet": 2200,
            "year_built": 2010,
            "description": "Spacious family home with modern amenities"
        },
        "amenities": {"pool": True, "garden": True, "garage": True},
        "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    }

# -------------------------
# Tests
# -------------------------
def test_create_property(property_service, sample_property_data, test_db):
    # Create a dummy user in the test database to satisfy the foreign key constraint
    user = User(id=str(sample_property_data["user_id"]), email="test@example.com", hashed_password="hashedpassword")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    prop_create = PropertyCreate(**sample_property_data)
    prop = property_service.create_property(prop_create)
    assert prop is not None
    assert prop.title == "Beautiful Family Home"
    assert prop.mongo_document_id is not None

def test_get_property_by_id(property_service, sample_property_data, test_db):
    # Create a dummy user for this test as well
    user = User(id=str(sample_property_data["user_id"]), email="test2@example.com", hashed_password="hashedpassword2")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    prop_create = PropertyCreate(**sample_property_data)
    prop = property_service.create_property(prop_create)

    result = property_service.get_property_by_id(prop.id)
    assert result is not None
    assert result["id"] == prop.id
    assert result["title"] == "Beautiful Family Home"

def test_get_user_properties(property_service, sample_user_id, sample_property_data, test_db):
    # Create a dummy user for this test
    user = User(id=str(sample_user_id), email="test3@example.com", hashed_password="hashedpassword3")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    # Create first property
    data1 = dict(sample_property_data)
    prop1 = property_service.create_property(PropertyCreate(**data1))

    # Create second property
    data2 = dict(sample_property_data)
    data2["title"] = "Luxury Apartment"
    prop2 = property_service.create_property(PropertyCreate(**data2))

    results = property_service.get_user_properties(sample_user_id)
    assert len(results) == 2
    titles = [r["title"] for r in results]
    assert "Beautiful Family Home" in titles
    assert "Luxury Apartment" in titles

def test_update_property(property_service, sample_property_data, test_db):
    # Create a dummy user for this test
    user = User(id=str(sample_property_data["user_id"]), email="test4@example.com", hashed_password="hashedpassword4")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    prop_create = PropertyCreate(**sample_property_data)
    prop = property_service.create_property(prop_create)

    updates = {
        "title": "Updated Home",
        "price": 375000.0,
        "details": {"bedrooms": 5, "bathrooms": 3}
    }

    updated = property_service.update_property(prop.id, updates)
    assert updated.title == "Updated Home"
    assert updated.price == 375000.0

def test_delete_property(property_service, sample_property_data, test_db):
    # Create a dummy user for this test
    user = User(id=str(sample_property_data["user_id"]), email="test5@example.com", hashed_password="hashedpassword5")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    prop_create = PropertyCreate(**sample_property_data)
    prop = property_service.create_property(prop_create)

    deleted = property_service.delete_property(prop.id)
    assert deleted is True

    # Confirm deletion
    result = property_service.get_property_by_id(prop.id)
    assert result is None
