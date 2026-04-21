from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)

class UserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=100)
    hashed_password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    username: str
    is_active: bool
    created_at: datetime

model_config = {"from_attributes": True}

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Tache Schemas ---    
class TacheBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    terminated: Optional[bool] = False

class TacheUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    terminated: Optional[bool] = None

class TacheCreate(TacheBase):
    user_id: int

class TacheResponse(TacheBase):
    id: int
    title: str
    description: str
    terminated: bool
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = {"from_attributes": True}