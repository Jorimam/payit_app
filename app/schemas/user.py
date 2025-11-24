from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
from typing import List, Optional, Dict
from ..enums import Gender
import re

class User(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    gender: str
    location: str

class UserCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    phone: str = Field(min_length=11, pattern=r"^\d{11,}$")
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str
    gender: Gender
    location: str = Field(min_length=3)

    @field_validator('phone')
    def phone_is_valid_numeric_value(cls, value):
        if value.isdigit() is not True:
            raise ValueError('phone number must be digits')
        return value

    @field_validator('password')
    def validate_password(cls, value:str):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value
    
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

class UserUpdateRequest(UserCreateRequest):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    location: Optional[str] = None

    @model_validator(mode='after')
    def clear_password_validation(self):
        return self
