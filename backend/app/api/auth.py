from fastapi import APIRouter, Depends, HTTPException, status,Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from db.database import get_db
from app.users.schemas import Token, UserCreate
from app.users.service import authenticate_user, create_user, get_user
from datetime import timedelta
from app.config import settings

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    existing_user = get_user(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = create_user(db, user_data)
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}