from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import UserCreate
from app.core.security import get_password_hash, verify_password
from db.database import get_db
from fastapi import Depends 


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password ,first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Remove the following incomplete function
# def get_current_user(
#     db: Session = Depends(get_db), 
#     token: str = Depends(oauth2_scheme)
# ) -> User:
#     user = get_user_by_token(db, token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials"
#         )
#     return user