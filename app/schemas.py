from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class UserCreate(BaseModel):
    username: str
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
    user_id: int | None = (
        None  # Optional - Admin can specify user, otherwise defaults to creator
    )


class RecordUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    description: str | None = None
    category: str | None = None
    date: datetime | None = None
    user_id: int | None = None  # Optional - Admin can reassign record to different user


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    description: str | None = None
    date: datetime
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
        use_enum_values = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    role: str
