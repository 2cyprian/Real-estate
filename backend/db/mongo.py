from pymongo import MongoClient
from app.config import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.properties = self.db.properties

    def insert_property(self, property_data: dict):
        """Insert a property document into MongoDB"""
        return self.properties.insert_one(property_data)

    def get_property_by_sql_id(self, sql_property_id: int):
        """Get property document by SQL property ID"""
        return self.properties.find_one({"sql_property_id": sql_property_id})

    def update_property(self, sql_property_id: int, update_data: dict):
        """Update property document"""
        return self.properties.update_one(
            {"sql_property_id": sql_property_id},
            {"$set": update_data}
        )

    def delete_property(self, sql_property_id: int):
        """Delete property document"""
        return self.properties.delete_one({"sql_property_id": sql_property_id})

# Global MongoDB instance
mongo_db = MongoDB()