from datetime import datetime
from json import JSONDecodeError
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from httpx import HTTPStatusError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
import schemas
from crud import user
from routes.api import deps
from schemas import UserCreate, UserUpdate
from utils.config import BOT_TOKEN
from utils.discord import exchange_code, get_auth_url, revoke_access_token
from utils.discord.user import get_user


router = APIRouter(prefix="/discord", tags=["discord"])


def auth_middleware(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
) -> dict:
    cookies = request.cookies

    if not cookies:
        return {}

    discord_user = get_user(cookies.get("token_type"), cookies.get("access_token"))

    if not discord_user:
        return {}

    discord_user_id = discord_user.get("id")
    curr_user = user.get_by_discord_id(db, discord_user_id)

    if not curr_user:
        new_user = UserCreate(discord_id=discord_user_id)
        user.create(db, obj_in=new_user)
    else:
        upd_user = UserUpdate(last_login=datetime.now())
        user.update(db, db_obj=curr_user, obj_in=upd_user)

    return discord_user


@router.get(
    "/users-by-bot/{user_id}",
    response_model=schemas.DiscordUser,
    response_model_exclude_unset=True,
)
def get_user_by_bot(user_id: int | str):
    """
    Read Discord user by Discord id. Request to Discord is sent from bot.
    :param user_id: Discord user id
    :return: Discord user
    """

    return get_user("Bot", BOT_TOKEN, user_id)


@router.get(
    "/users/@me",
    response_model=schemas.DiscordUser,
)
def get_self(discord_user: Annotated[dict, Depends(auth_middleware)]):
    """
    Get data from self Discord account.
    """
    if not discord_user:
        raise HTTPException(401, detail="Not authorized.")
    return discord_user


@router.get("/login")
def login_to_discord() -> Response:
    """
    Login to Discord.
    """
    return RedirectResponse(get_auth_url())


@router.get("/logout")
def logout(request: Request, response: Response):
    """
    Logout from Discord.
    """
    cookies = request.cookies
    if access_token := cookies.get("access_token"):
        revoke_access_token(access_token)

    for cookie in cookies:
        response.delete_cookie(cookie, httponly=True)


@router.get("/callback")
def get_auth_callback(
    code: str,
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(deps.get_db)],
):
    """
    Discord auth callback.
    """
    try:
        cookies: dict = exchange_code(code)
    except HTTPStatusError as err:
        resp_json: dict | str

        try:
            resp_json = err.response.json()
        except JSONDecodeError:
            resp_json = err.response.text

        raise HTTPException(err.response.status_code, detail=resp_json)

    yield auth_middleware(request, db)

    expires = cookies.pop("expires_in")

    for cookie in cookies.keys():
        response.set_cookie(cookie, cookies.get(cookie), expires=expires, httponly=True)
