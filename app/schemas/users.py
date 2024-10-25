from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime

class UsersCreate(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email_address: EmailStr
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    username: str
    email_address: EmailStr

    class Config:
        from_attributes = True

    
