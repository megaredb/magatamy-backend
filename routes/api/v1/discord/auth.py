from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

import schemas
from crud import user
from routes.api import deps
from utils.discord.user import get_guild_member


async def auth_middleware(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
) -> schemas.DiscordGuildMember | None:
    cookies = request.cookies

    guild_member: schemas.DiscordGuildMember | None = None

    if cookies.get("access_token"):
        guild_member = await get_guild_member(
            cookies.get("token_type"), cookies.get("access_token")
        )

    if not guild_member:
        raise HTTPException(401, "Not authorized.")

    discord_user_id = guild_member.user.id
    curr_user = user.get_by_discord_id(db, discord_user_id)

    if not curr_user:
        new_user = schemas.UserCreate(discord_id=discord_user_id)
        user.create(db, obj_in=new_user)
    else:
        upd_user = schemas.UserUpdate(last_login=datetime.now())
        user.update(db, db_obj=curr_user, obj_in=upd_user)

    return guild_member


async def only_moderator(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
) -> schemas.DiscordGuildMember:
    discord_user = await auth_middleware(request, db)

    if not discord_user.is_moderator():
        raise HTTPException(401, "Not authorized.")

    return discord_user


async def only_admin(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
) -> schemas.DiscordGuildMember:
    discord_user = await auth_middleware(request, db)

    if not discord_user.is_admin():
        raise HTTPException(401, "Not authorized.")

    return discord_user
