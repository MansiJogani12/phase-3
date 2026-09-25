from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    email: EmailStr
    username: str
    password: Optional[str] = None
    githubId: Optional[str] = None
    githubAccessToken: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: Optional[str] = None
    githubId: Optional[str] = None
    githubAccessToken: Optional[str] = None
