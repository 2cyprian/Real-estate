from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users.schemas import UserOut, UserCreate # Changed User to UserOut
from app.users.service import get_user, create_user
from db.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED) # Changed User to UserOut
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/me", response_model=UserOut) # Changed User to UserOut
def read_users_me(current_user: UserOut = Depends(get_current_user)): # Changed User to UserOut
    return current_user