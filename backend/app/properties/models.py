from sqlalchemy import Column, BIGINT, String, Enum, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from db.database import Base

class Property(Base):
    """
    SQLAlchemy model for the 'properties' table.
    
    This model holds the core, filterable, and relational data for a property listing.
    """
    __tablename__ = "properties"

    # Define columns, matching your SQL schema
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    
    # Using UUID for user_id with proper foreign key relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(255), nullable=False)
    
    property_type = Column(
        Enum('house', 'apartment', 'land', 'commercial', name='property_type_enum'),
        nullable=False,
        index=True
    )
    
    price = Column(DECIMAL(15, 2), nullable=False, index=True)
    
    status = Column(
        Enum('available', 'rented', 'sold', name='property_status_enum'),
        nullable=False,
        default='available',
        index=True
    )
    
    # Let the database handle the default timestamp
    created_at = Column(TIMESTAMP, server_default=func.now())

    # This field is crucial for linking to the NoSQL document
    mongo_document_id = Column(String(24), unique=True, nullable=True)

    def __repr__(self):
        return f"<Property(id={self.id}, title='{self.title}')>"