from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from httpx import get, post, delete
from starlette.responses import Response

import schemas
from routes.api.v1.discord import auth_middleware
from routes.api.v1.discord.auth import only_moderator
from schemas import DiscordGuildMember
from utils import config

router = APIRouter(prefix="/minecraft", tags=["minecraft"])


@router.get(
    "/money",
    response_model=schemas.MCUserData,
)
def get_money(discord_user: Annotated[DiscordGuildMember, Depends(auth_middleware)]):
    username = str(discord_user.nick)

    resp = get(
        "%s/money/%s" % (config.MAIN_MC_SERVER_HOST, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(404, detail="Minecraft user not found.")

    user_data = schemas.MCUserData(username=username, money=resp.json().get("money"))

    return user_data


@router.get(
    "/online",
    response_model=schemas.MCOnline,
)
def get_online_count():
    resp = get(
        "%s/online" % config.MAIN_MC_SERVER_HOST,
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(404, detail="Minecraft server not found.")

    online_data = schemas.MCOnline(count=resp.json().get("count"))

    return online_data


@router.post(
    "/whitelist/{username}",
)
def post_to_whitelist(
    username: str, _deps: Annotated[DiscordGuildMember, Depends(only_moderator)]
):
    resp = post(
        "%s/whitelist/%s" % (config.MAIN_MC_SERVER_HOST, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(400)

    return Response()


@router.delete(
    "/whitelist/{username}",
)
def remove_from_whitelist(
    username: str, _deps: Annotated[DiscordGuildMember, Depends(only_moderator)]
):
    resp = delete(
        "%s/whitelist/%s" % (config.MAIN_MC_SERVER_HOST, username),
        headers={"Authorization": config.MC_SERVER_KEY},
    )

    if resp.status_code != 200:
        raise HTTPException(400)

    return Response()
