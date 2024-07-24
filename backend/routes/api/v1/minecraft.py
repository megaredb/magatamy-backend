from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from httpx import get, post, delete
from starlette.responses import Response

from backend import schemas
from backend.routes.api.v1.discord import auth_middleware
from backend.routes.api.v1.discord.auth import only_moderator
from backend.schemas import DiscordGuildMember
from backend.utils import config
from backend.utils.discord.user import send_message
from backend.utils.minecraft import ServerEnum, SERVERS

router = APIRouter(prefix="/minecraft", tags=["minecraft"])


@router.get(
    "/{server}/money",
    response_model=schemas.MCUserData,
)
def get_money(
    server: ServerEnum,
    discord_user: Annotated[DiscordGuildMember, Depends(auth_middleware)],
):
    username = str(discord_user.nick)
    server_host = SERVERS[server]

    resp = get(
        "%s/money/%s" % (server_host, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(404, detail="Minecraft user not found.")

    user_data = schemas.MCUserData(username=username, money=resp.json().get("money"))

    return user_data


@router.get(
    "/{server}/online",
    response_model=schemas.MCOnline,
)
def get_online_count(
    server: ServerEnum,
):
    server_host = SERVERS[server]

    resp = get(
        "%s/online" % server_host,
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(404, detail="Minecraft server not found.")

    online_data = schemas.MCOnline(count=resp.json().get("count"))

    return online_data


@router.post(
    "/{server}/whitelist/{username}",
)
async def post_to_whitelist(
    server: ServerEnum,
    username: str,
    guild_member: Annotated[DiscordGuildMember, Depends(only_moderator)],
):
    server_host = SERVERS[server]

    resp = post(
        "%s/whitelist/%s" % (server_host, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    msg = schemas.discord.CreateDiscordMessage()
    msg.embeds = [
        {
            "title": "Изменение белого списка",
            "description": (
                f"Пользователь <@{guild_member.user.id}> добавляет в белый список {username} на сервере {server}"
            ),
        }
    ]
    await send_message(config.DISCORD_LOG_CHANNEL_ID, msg, False)

    if resp.status_code != 200:
        raise HTTPException(400)

    return Response()


@router.delete(
    "/{server}/whitelist/{username}",
)
async def remove_from_whitelist(
    server: ServerEnum,
    username: str,
    guild_member: Annotated[DiscordGuildMember, Depends(only_moderator)],
):
    server_host = SERVERS[server]

    resp = delete(
        "%s/whitelist/%s" % (server_host, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    msg = schemas.discord.CreateDiscordMessage()
    msg.embeds = [
        {
            "title": "Изменение белого списка",
            "description": (
                f"Пользователь <@{guild_member.user.id}> удаляет из белого списка {username} на сервере {server}"
            ),
        }
    ]
    await send_message(config.DISCORD_LOG_CHANNEL_ID, msg, False)

    if resp.status_code != 200:
        raise HTTPException(400)

    return Response()
