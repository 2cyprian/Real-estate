from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from uuid import UUID as PyUUID
from datetime import date, datetime


# --- Sub-models for the MongoDB Document ---


class PropertyBase(BaseModel):
    title: str
    property_type: str
    price: float
    status: str
    pass

class Coordinates(BaseModel):
    lat: float
    lng: float

class Location(BaseModel):
    address: str
    coordinates: Coordinates
    street_address: Optional[str] = None

class Details(BaseModel):
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    kitchens: Optional[int] = None
    lounges: Optional[int] = None
    dining_rooms: Optional[int] = None
    offices: Optional[int] = None
    erf_size_m2: Optional[int] = None
    floor_size_m2: Optional[int] = None
    lease_period_months: Optional[int] = None
    deposit_required: Optional[float] = None
    occupation_date: Optional[date] = None

class Amenities(BaseModel):
    pets_allowed: Optional[bool] = None
    furnished: Optional[bool] = None
    temperature_controls: Optional[int] = None  # could later become Enum

class Features(BaseModel):
    pool: Optional[bool] = None
    balcony: Optional[bool] = None
    flatlet: Optional[bool] = None
    retirement: Optional[bool] = None
    repossessed: Optional[bool] = None
    on_show: Optional[bool] = None
    security_estate_cluster: Optional[bool] = None

class ExternalFeatures(BaseModel):
    parking: Optional[int] = None
    gardens: Optional[int] = None

class PointOfInterest(BaseModel):
    name: str
    distance_km: float

# 🔥 Make POIs dynamic instead of fixed categories
class PointsOfInterest(BaseModel):
    categories: Dict[str, List[PointOfInterest]] = {}

class Media(BaseModel):
    url: str
    type: Literal['image', 'video']

# --- Main MongoDB Document Schema ---

class PropertyDetailsMongo(BaseModel):
    sql_property_id: Optional[PyUUID] = None  # linked after SQL insert
    location: Location
    details: Optional[Details] = None
    amenities: Optional[Amenities] = None
    features: Optional[Features] = None
    external_features: Optional[ExternalFeatures] = None
    points_of_interest: Optional[PointsOfInterest] = None
    media: List[Media] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- API Schemas ---

class PropertyCreate(BaseModel):
    # Core SQL fields
    user_id: Optional[PyUUID] = None # Make user_id optional
    title: str
    property_type: Literal['house', 'apartment', 'land', 'commercial']
    price: float
    status: Literal['available', 'rented', 'sold'] = 'available'

    # Directly attach Mongo-style fields (instead of double nesting)
    location: Location
    details: Optional[Details] = None
    amenities: Optional[Amenities] = None
    features: Optional[Features] = None
    external_features: Optional[ExternalFeatures] = None
    points_of_interest: Optional[PointsOfInterest] = None
    media: List[Media] = []

class PropertyResponse(BaseModel):
    id: PyUUID
    user_id: PyUUID
    title: str
    property_type: str
    price: float
    status: str
    mongo_document_id: Optional[str] = None # Add this field

    # MongoDB fields
    location: Optional[Location] = None  # Make location optional
    details: Optional[Details] = None
    amenities: Optional[Amenities] = None
    features: Optional[Features] = None
    external_features: Optional[ExternalFeatures] = None
    points_of_interest: Optional[PointsOfInterest] = None
    media: List[Media] = []

    class Config:
        from_attributes = True # Use from_attributes instead of orm_mode for Pydantic v2

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    property_type: Optional[Literal['house', 'apartment', 'land', 'commercial']] = None
    price: Optional[float] = None
    status: Optional[Literal['available', 'rented', 'sold']] = None
    location: Optional[Location] = None
    details: Optional[Details] = None
    amenities: Optional[Amenities] = None
    features: Optional[Features] = None
    external_features: Optional[ExternalFeatures] = None
    points_of_interest: Optional[PointsOfInterest] = None
    media: Optional[List[Media]] = None

class Property(PropertyBase):
    id: int
    owner_id: int
    

    class Config:
        orm_mode = True  # allows SQLAlchemy objects to be converted automatically
