from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: int
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str # Change this from int to str
    role:str
    
    class Config:
        from_attributes=True

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
