from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.security import PasswordPolicy

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str, info):
        valid, err = PasswordPolicy.validate(v)
        if not valid:
            raise ValueError(err)
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
