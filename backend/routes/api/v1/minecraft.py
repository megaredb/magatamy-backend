from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from httpx import get

from backend import schemas
from backend.routes.api.v1.discord.auth import only_moderator
from backend.schemas import DiscordGuildMember
from backend.utils import config
from backend.utils.discord.user import send_message
from backend.utils.minecraft import ServerEnum, SERVERS

router = APIRouter(prefix="/minecraft", tags=["minecraft"])


@router.get("/online")
def get_online_count():
    resp = get(
        f"{config.PROXY_SERVER_HOST}/api/getOnline?secret_key={config.PROXY_SERVER_KEY}",
    )

    if resp.status_code != 200:
        raise HTTPException(404, detail="Minecraft server not found.")

    online_data = resp.json()

    online_data["labels"] = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    ]

    curr_day = datetime.now().isoweekday()

    online_data["labels"] = (
        online_data["labels"][curr_day:] + online_data["labels"][:curr_day]
    )

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

    return Response()
