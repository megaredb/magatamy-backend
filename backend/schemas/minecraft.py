from pydantic import BaseModel


class MCUserData(BaseModel):
    username: str
    money: int


class MCOnline(BaseModel):
    count: int
