from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "student"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class EventCreate(BaseModel):
    title: str
    description: str
    category: str
    venue: str
    organizer_id: str
    start_time: datetime
    end_time: datetime
    capacity: int = 100
    banner_url: Optional[str] = None


class EventResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    venue: str
    organizer_id: str
    start_time: datetime
    end_time: datetime
    capacity: int
    status: str

    class Config:
        from_attributes = True