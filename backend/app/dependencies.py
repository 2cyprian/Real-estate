from db.database import SessionLocal
from db.mongo import get_mongo_db_async # Changed from get_mongo_client
from app.core.security import get_current_active_user, oauth2_scheme # Import oauth2_scheme
from app.users.service import get_user
from app.users.repository import UserRepository
from app.users.schemas import UserResponse
from fastapi import Depends
from sqlalchemy.orm import Session # Add this import
from db.database import get_db
from db.mongo import get_mongo_db_async
from app.core.security import get_current_active_user, oauth2_scheme
from app.users.service import get_user
from app.users.repository import UserRepository
from app.users.schemas import UserResponse
from fastapi import Depends
from app.users.models import User # Add this import

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the MongoDB client
def get_mongo_db():
    client = get_mongo_client()
    try:
        yield client.get_database()
    finally:
        client.close()

# Dependency to get the current user (re-using existing security function)
async def get_current_user_from_token(
    current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse.model_validate(current_user)