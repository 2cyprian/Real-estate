from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
from pymongo.server_api import ServerApi

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI, server_api=ServerApi('1'))
        self.db: AsyncIOMotorDatabase = self.client[settings.MONGO_DB_NAME]
        self.properties = self.db.properties

    async def insert_property(self, property_data: dict):
        """Insert a property document into MongoDB"""
        return await self.properties.insert_one(property_data)

    async def get_property_by_sql_id(self, sql_property_id: str): # Changed type to str for UUID
        """Get property document by SQL property ID"""
        return await self.properties.find_one({"sql_property_id": sql_property_id})

    async def update_property(self, sql_property_id: str, update_data: dict): # Changed type to str
        """Update property document"""
        return await self.properties.update_one(
            {"sql_property_id": sql_property_id},
            {"$set": update_data}
        )

    async def delete_property(self, sql_property_id: str): # Changed type to str
        """Delete property document"""
        return await self.properties.delete_one({"sql_property_id": sql_property_id})

# Global MongoDB instance
mongo_db = MongoDB()

async def get_mongo_db_async() -> AsyncIOMotorDatabase:
    """Dependency that provides the MongoDB database instance."""
    return mongo_db.db