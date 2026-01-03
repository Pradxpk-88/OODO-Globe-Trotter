from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Trip Models
class TripCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    destination: str = Field(..., min_length=1, max_length=200)
    start_date: date
    end_date: date
    description: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)

    @validator('end_date')
    def end_date_must_be_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

    class Config:
        from_attributes = True

class TripUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    destination: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)

    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    id: int
    title: str
    destination: str
    start_date: date
    end_date: date
    description: Optional[str] = None
    budget: Optional[float] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Stop Models
class StopCreate(BaseModel):
    trip_id: int
    location: str = Field(..., min_length=1, max_length=200)
    arrival_date: date
    departure_date: date
    notes: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)

    @validator('departure_date')
    def departure_must_be_after_arrival(cls, v, values):
        if 'arrival_date' in values and v < values['arrival_date']:
            raise ValueError('departure_date must be after arrival_date')
        return v

    class Config:
        from_attributes = True

class StopUpdate(BaseModel):
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    arrival_date: Optional[date] = None
    departure_date: Optional[date] = None
    notes: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)

    class Config:
        from_attributes = True

class StopResponse(BaseModel):
    id: int
    trip_id: int
    location: str
    arrival_date: date
    departure_date: date
    notes: Optional[str] = None
    order: int
    created_at: datetime

    class Config:
        from_attributes = True

# Activity Models
class ActivityCreate(BaseModel):
    stop_id: int
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True

class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    id: int
    stop_id: int
    name: str
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Cost Models
class CostCreate(BaseModel):
    trip_id: int
    stop_id: Optional[int] = None
    category: str = Field(..., max_length=50)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    description: Optional[str] = None
    date: date

    class Config:
        from_attributes = True

class CostUpdate(BaseModel):
    category: Optional[str] = Field(None, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    description: Optional[str] = None
    date: Optional[date] = None

    class Config:
        from_attributes = True

class CostResponse(BaseModel):
    id: int
    trip_id: int
    stop_id: Optional[int] = None
    category: str
    amount: float
    currency: str
    description: Optional[str] = None
    date: date
    created_at: datetime

    class Config:
        from_attributes = True

# Share Models
class ShareCreate(BaseModel):
    trip_id: int
    shared_with_email: EmailStr
    permission_level: str = Field(default="view", pattern="^(view|edit)$")

    class Config:
        from_attributes = True

class ShareResponse(BaseModel):
    id: int
    trip_id: int
    shared_by_user_id: int
    shared_with_user_id: int
    permission_level: str
    created_at: datetime

    class Config:
        from_attributes = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None