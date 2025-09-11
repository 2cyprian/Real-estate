from fastapi import FastAPI
from app.api import auth # Keep this for auth.router
from app.users.router import router as users_router # Correct import for users_router
from app.properties.router import router as properties_router
from db.database import Base, engine
from db.mongo import mongo_db # Keep this import

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate API")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(properties_router, prefix="/properties", tags=["properties"])

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    # Test MongoDB connection
    try:
        await mongo_db.client.admin.command('ping') # Changed to await
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

@app.get("/")
async def root():
    return {
        "message": "Real Estate API",
        "databases": {
            "postgres": "connected",
            "mongodb": "connected" if mongo_db.client else "disconnected"
        }
    }


