from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from schemas.ticket.form import Form


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
    purchased_forms: List[Form]

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
