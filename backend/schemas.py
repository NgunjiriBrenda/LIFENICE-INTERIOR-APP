from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    phone_number: Optonal[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
            return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    phone_number: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

