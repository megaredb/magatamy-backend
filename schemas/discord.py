from typing import Optional, List
from pydantic import BaseModel

from utils import config
from utils.config import DISCORD_ADMIN_ROLE_ID, DISCORD_MODERATOR_ROLE_ID


class DiscordUser(BaseModel):
    id: str
    username: str
    global_name: Optional[str] = None
    discriminator: str
    avatar: str
    flags: int
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    premium_type: int
    public_flags: int


class DiscordGuildMember(BaseModel):
    user: Optional[DiscordUser] = None
    nick: Optional[str] = None
    avatar: Optional[str] = None
    roles: List[str]

    def is_moderator(self):
        return self.is_admin() or DISCORD_MODERATOR_ROLE_ID in self.roles

    def is_admin(self):
        return self.user.id in config.ADMINS or DISCORD_ADMIN_ROLE_ID in self.roles


class CreateDiscordMessage(BaseModel):
    content: Optional[str] = None
    embeds: Optional[list[dict]] = []
    attachments: Optional[list[dict]] = []
