from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import PyMongoError
import logging

from app.properties.models import Property
from app.properties.schema import PropertyCreate, PropertyResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

class PropertyService:
    """Service class for handling property operations across PostgreSQL and MongoDB."""

    def __init__(self, db: Session, mongo_db: AsyncIOMotorDatabase):
        self.db = db
        self.mongo_db = mongo_db
        self.properties_collection = self.mongo_db.properties # Get the collection here

    async def create_property(self, property_data: PropertyCreate) -> PropertyResponse:
        try:
            # Create SQL property
            sql_property_id = uuid4()
            db_property = Property(
                id=sql_property_id,
                user_id=property_data.user_id,
                title=property_data.title,
                property_type=property_data.property_type,
                price=property_data.price,
                status=property_data.status,
            )
            self.db.add(db_property)
            self.db.commit()
            self.db.refresh(db_property)

            # Prepare data for MongoDB
            mongo_data = property_data.model_dump(exclude_unset=True)
            mongo_data["sql_property_id"] = str(sql_property_id) # Link to SQL ID
            
            # Convert user_id to string for MongoDB
            if property_data.user_id:
                mongo_data["user_id"] = str(property_data.user_id)

            # Insert into MongoDB
            # Corrected: Use insert_one on the collection
            mongo_result = await self.properties_collection.insert_one(mongo_data)
            mongo_document_id = str(mongo_result.inserted_id)

            # Update SQL property with MongoDB document ID
            db_property.mongo_document_id = mongo_document_id
            self.db.commit()
            self.db.refresh(db_property)

            # Combine data for response
            # Convert db_property to a dictionary and merge with mongo_data
            # Ensure all fields expected by PropertyResponse are present
            combined_data = db_property.__dict__.copy()
            combined_data.update(mongo_data)
            
            # Remove SQLAlchemy internal state if present
            combined_data.pop('_sa_instance_state', None)

            # Create PropertyResponse from the combined data
            response_obj = PropertyResponse.model_validate(combined_data)

            return response_obj
        except Exception as e:
            self.db.rollback()
            print(f"Failed to create property: {e}")
            raise e

    async def get_property_by_id(self, property_id: UUID) -> Optional[PropertyResponse]:
        """Fetch one property from both SQL and Mongo."""
        try:
            db_property = self.db.query(Property).filter(Property.id == property_id).first()
            if not db_property:
                return None

            # Assuming get_property_by_sql_id returns a dictionary
            mongo_document = await self.properties_collection.find_one({"sql_property_id": str(property_id)})
            if not mongo_document:
                logger.warning(f"Property {property_id} found in SQL but not in MongoDB")
                return None

            # Create PropertyResponse from db_property
            response_obj = PropertyResponse.model_validate(db_property)

            # Update with MongoDB fields from mongo_document
            # Remove _id from mongo_document if present, as it's not in PropertyResponse
            if "_id" in mongo_document:
                del mongo_document["_id"]
            
            # Remove sql_property_id from mongo_document if present, as it's already handled by db_property.id
            if "sql_property_id" in mongo_document:
                del mongo_document["sql_property_id"]

            # Update response_obj with remaining mongo_document fields
            for key, value in mongo_document.items():
                if hasattr(response_obj, key):
                    setattr(response_obj, key, value)

            return response_obj

        except (SQLAlchemyError, PyMongoError) as e:
            logger.error(f"Failed to get property {property_id}: {e}")
            return None

    async def get_user_properties(self, user_id: UUID) -> List[PropertyResponse]:
        """Fetch all properties owned by a user."""
        try:
            db_properties = self.db.query(Property).filter(Property.user_id == user_id).all()
            result = []

            for db_property in db_properties:
                mongo_document = self.mongo_db.get_property_by_sql_id(str(db_property.id))
                item = {
                    "id": db_property.id,
                    "user_id": db_property.user_id,
                    "title": db_property.title,
                    "property_type": db_property.property_type,
                    "price": float(db_property.price) if db_property.price else None,
                    "status": db_property.status,
                    "created_at": db_property.created_at,
                    "mongo_document_id": db_property.mongo_document_id,
                }
                if mongo_document:
                    item.update(mongo_document)
                result.append(item)

            return result

        except (SQLAlchemyError, PyMongoError) as e:
            logger.error(f"Failed to get properties for user {user_id}: {e}")
            return []

    async def update_property(self, property_id: UUID, update_data: dict) -> Optional[PropertyResponse]:
        """Update property in both SQL and MongoDB."""
        try:
            db_property = self.db.query(Property).filter(Property.id == property_id).first()
            if not db_property:
                return None

            sql_updates = {}
            mongo_updates = {}

            for key, value in update_data.items():
                if hasattr(Property, key):
                    sql_updates[key] = value
                else:
                    mongo_updates[key] = value

            for k, v in sql_updates.items():
                setattr(db_property, k, v)

            if mongo_updates and db_property.mongo_document_id:
                self.mongo_db.update_property(db_property.mongo_document_id, mongo_updates)

            self.db.commit()
            self.db.refresh(db_property)
            return db_property

        except (SQLAlchemyError, PyMongoError) as e:
            self.db.rollback()
            logger.error(f"Failed to update property {property_id}: {e}")
            return None

    async def delete_property(self, property_id: UUID) -> bool:
        """Delete property from both SQL and MongoDB."""
        try:
            db_property = self.db.query(Property).filter(Property.id == property_id).first()
            if not db_property:
                return False

            if db_property.mongo_document_id:
                self.mongo_db.delete_property(db_property.mongo_document_id)

            self.db.delete(db_property)
            self.db.commit()
            return True

        except (SQLAlchemyError, PyMongoError) as e:
            self.db.rollback()
            logger.error(f"Failed to delete property {property_id}: {e}")
            return False

    def search_properties(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search properties using SQL and Mongo filters."""
        try:
            query = self.db.query(Property)

            # SQL filters
            if "property_type" in filters:
                query = query.filter(Property.property_type == filters["property_type"])
            if "min_price" in filters:
                query = query.filter(Property.price >= filters["min_price"])
            if "max_price" in filters:
                query = query.filter(Property.price <= filters["max_price"])
            if "status" in filters:
                query = query.filter(Property.status == filters["status"])

            db_properties = query.all()
            results = []

            for db_property in db_properties:
                mongo_document = self.mongo_db.get_property_by_sql_id(str(db_property.id))
                if not mongo_document:
                    continue

                include = True
                if "location" in filters and filters["location"]:
                    loc_filter = filters["location"].lower()
                    mongo_loc = mongo_document.get("location", {})
                    if not any(
                        mongo_loc.get(field, "").lower() == loc_filter
                        for field in ["address", "street_address"]
                    ):
                        include = False

                if include:
                    item = {
                        "id": db_property.id,
                        "user_id": db_property.user_id,
                        "title": db_property.title,
                        "property_type": db_property.property_type,
                        "price": float(db_property.price) if db_property.price else None,
                        "status": db_property.status,
                        "created_at": db_property.created_at,
                        "mongo_document_id": db_property.mongo_document_id,
                    }
                    item.update(mongo_document)
                    results.append(item)

            return results

        except (SQLAlchemyError, PyMongoError) as e:
            logger.error(f"Failed to search properties: {e}")
            return []
