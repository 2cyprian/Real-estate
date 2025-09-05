from fastapi import FastAPI
from app.api import auth, users
from app.properties.router import router as properties_router
from app.db.database import Base, engine
from app.db.mongo import mongo_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate API")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(properties_router, prefix="/properties", tags=["properties"])

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    # Test MongoDB connection
    try:
        mongo_db.client.admin.command('ping')
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

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}

