# Import necessary SQLAlchemy components and utilities
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB  # PostgreSQL-specific types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from db.database import Base


# Create base class for declarative models

class User(Base):
    """
    SQLAlchemy model for users table with the following fields:
    - id: UUID primary key
    - email: Unique email address
    - hashed_password: Encrypted password
    - first_name: User's first name
    - last_name: User's last name
    - phone_number: User's phone number
    - role: User's role (owner, agent, buyer, tenant, admin)
    - created_at: Timestamp of user creation
    - updated_at: Timestamp of last update
    """
    __tablename__ = 'users'

    # Primary key using UUID instead of integer
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User authentication fields
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # User profile fields
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, nullable=True) # Changed to String to accommodate leading zeros and other formats
    role = Column(Enum('owner', 'agent', 'buyer', 'tenant', 'admin', name='user_role_enum'), default='tenant', nullable=False)
    is_active = Column(Boolean, default=True) # Add this line
    
    # Audit timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        """String representation of User object"""
        return f"<User(email='{self.email}', first_name='{self.first_name}')>"