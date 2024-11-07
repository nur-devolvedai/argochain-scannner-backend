# app/models/user.py
from bson import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    hashed_password: str
