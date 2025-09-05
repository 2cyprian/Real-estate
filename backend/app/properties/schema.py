from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import UUID as PyUUID
from datetime import date, datetime

# --- Sub-models for the MongoDB Document ---

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
    pets_allowed: bool
    furnished: bool
    temperature_controls: int # Could be an enum later

class Features(BaseModel):
    pool: bool
    balcony: bool
    flatlet: bool
    retirement: bool
    repossessed: bool
    on_show: bool
    security_estate_cluster: bool

class ExternalFeatures(BaseModel):
    parking: int
    gardens: int

class PointOfInterest(BaseModel):
    name: str
    distance_km: float

class PointsOfInterest(BaseModel):
    education: List[PointOfInterest] = []
    health: List[PointOfInterest] = []
    shopping: List[PointOfInterest] = []

class Media(BaseModel):
    url: str
    type: Literal['image', 'video']

# --- Main MongoDB Document Schema ---

class PropertyDetailsMongo(BaseModel):
    sql_property_id: Optional[int] = None # Will be populated after SQL insert
    location: Location
    details: Details
    amenities: Amenities
    features: Features
    external_features: ExternalFeatures
    points_of_interest: PointsOfInterest
    media: List[Media]
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- API Schemas ---

# 1. Schema for Creating a Property (what the API receives)

class PropertyCreate(BaseModel):
    # Core SQL fields
    user_id: PyUUID
    title: str
    property_type: Literal['house', 'apartment', 'land', 'commercial']
    price: float
    status: Literal['available', 'rented', 'sold'] = 'available'
    # The entire nested MongoDB document
    details: PropertyDetailsMongo

# 2. Schema for Responding with a Property (what the API sends back)

class PropertyResponse(BaseModel):
    # Core SQL fields
    id: int
    user_id: PyUUID
    title: str
    property_type: str
    price: float
    status: str
    created_at: datetime
    # The nested MongoDB details
    details: PropertyDetailsMongo

    class Config:
        orm_mode = True # This allows Pydantic to read data from ORM models (like SQLAlchemy)