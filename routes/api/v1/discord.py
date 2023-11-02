from json import JSONDecodeError
from typing import Union

from fastapi import APIRouter, HTTPException
from httpx import get
import schemas
from discordbot.config import bot_token

router = APIRouter(prefix="/discord")


@router.get(
    "/users/{user_id}", response_model=Union[schemas.DiscordUser, schemas.DiscordError]
)
def read_user(user_id: int):
    try:
        request = get(
            f"https://discord.com/api/v9/users/{user_id}",
            headers={"Authorization": f"Bot {bot_token}"},
        ).json()

        return request
    except (JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=502, detail="Discord interaction error")
