from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re
from .models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.STUDENT
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @field_validator("full_name")
    @classmethod
    def sanitize_name(cls, v: str):
        if v:
            # Strip HTML tags and extra whitespace (prevent XSS)
            v = re.sub(r'<[^>]*>', '', v)
            v = v.strip()
        return v

    @field_validator("phone_number")
    @classmethod
    def sanitize_phone(cls, v: str):
        if v:
            # Only allow digits and common phone characters (prevent injection/garbage)
            v = re.sub(r'[^\d+\-\(\) ]', '', v)
            v = v.strip()
        return v

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
