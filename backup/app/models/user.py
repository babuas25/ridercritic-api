from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    uid: str
    email_verified: bool = False
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    roles: List[str] = Field(default_factory=list)


class UserResponse(UserBase):
    uid: str
    email_verified: bool
    roles: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
