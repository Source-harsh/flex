from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class PropertyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price_per_hour: Optional[float] = None
    dimensions: Optional[str] = None


class PropertyOut(PropertyCreate):
    id: int
    provider_id: int

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    property_id: int
    start_time: datetime
    end_time: datetime
    total_price: float


class BookingOut(BaseModel):
    id: int
    property_id: int
    renter_id: int
    start_time: datetime
    end_time: datetime
    total_price: float
    status: str

    class Config:
        orm_mode = True
