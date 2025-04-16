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


class UserResponse(UserBase):
    uid: str
    email_verified: bool = False
    disabled: bool = False
    roles: List[str] = ["user"]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
