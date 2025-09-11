from typing import Optional
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from app.core.password_utils import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            hashed_password=get_password_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
