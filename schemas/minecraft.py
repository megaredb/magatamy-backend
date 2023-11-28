from pydantic import BaseModel


class MCUserData(BaseModel):
    username: str
    money: int
