from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RecordCreate(BaseModel):
    amount: float
    type: str
    description: str | None = None
    category: str
    date: datetime


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    description: str | None = None
    date: datetime
    craeted_at: datetime
    user_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    role: str
