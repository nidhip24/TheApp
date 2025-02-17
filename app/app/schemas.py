from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str


class User(UserCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
