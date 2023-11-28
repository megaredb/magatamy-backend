from typing import Optional

from pydantic import BaseModel

from schemas import minecraft


# class DiscordError(BaseModel):
#     message: str
#     code: int


class DiscordUser(BaseModel):
    id: str
    username: str
    global_name: str
    discriminator: str
    avatar: str
    flags: int
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    premium_type: int
    public_flags: int
