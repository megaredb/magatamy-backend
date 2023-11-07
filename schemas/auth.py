from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    discord_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    last_login: Optional[datetime] = None


class UserInDBBase(UserBase):
    id: str
    created_at: datetime
    last_login: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
