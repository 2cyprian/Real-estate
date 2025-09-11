from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.properties.schema import PropertyCreate, PropertyResponse, PropertyUpdate
from app.properties.services import PropertyService
from db.database import get_db
from db.mongo import get_mongo_db_async # Changed import
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.dependencies import get_current_user_from_token # Import get_current_user_from_token
from app.users.schemas import UserResponse # Import UserResponse to type hint current_user

router = APIRouter()

@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db_async),
    current_user: UserResponse = Depends(get_current_user_from_token) # Add this dependency
):
    # Assign the user_id from the authenticated user
    property_data.user_id = current_user.id
    
    service = PropertyService(db, mongo_db)
    try:
        new_property = await service.create_property(property_data)
        # Fetch the full property details including MongoDB fields for the response
        full_property_details = await service.get_property_by_id(new_property.id) # Add await here
        if not full_property_details:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created property details."
            )
        return full_property_details
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_by_id( # Changed to async def
    property_id: UUID,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db_async) # Changed dependency
):
    service = PropertyService(db, mongo_db)
    property_details = await service.get_property_by_id(property_id) # Changed to await
    if not property_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property_details

@router.get("/user/{user_id}", response_model=List[PropertyResponse])
async def get_user_properties( # Changed to async def
    user_id: UUID,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db_async) # Changed dependency
):
    service = PropertyService(db, mongo_db)
    properties = await service.get_user_properties(user_id) # Changed to await
    return properties

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property( # Changed to async def
    property_id: UUID,
    update_data: PropertyUpdate,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db_async) # Changed dependency
):
    service = PropertyService(db, mongo_db)
    updated_property = await service.update_property(property_id, update_data.model_dump(exclude_unset=True)) # Changed to await
    if not updated_property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    # Fetch the full property details including MongoDB fields for the response
    full_property_details = await service.get_property_by_id(updated_property.id) # Add await here
    if not full_property_details:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve updated property details."
        )
    return full_property_details

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property( # Changed to async def
    property_id: UUID,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db_async) # Changed dependency
):
    service = PropertyService(db, mongo_db)
    if not await service.delete_property(property_id): # Changed to await
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return {"message": "Property deleted successfully"}
