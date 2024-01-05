from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from httpx import get

import schemas
from routes.api.v1.discord import auth_middleware
from utils import config

router = APIRouter(prefix="/minecraft", tags=["minecraft"])


@router.get(
    "/money",
    response_model=schemas.MCUserData,
)
def get_money(discord_user: Annotated[dict, Depends(auth_middleware)]):
    username = str(discord_user.get("username"))

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
