from json import JSONDecodeError
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache
from httpx import HTTPStatusError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from backend import schemas
from backend.routes.api import deps
from backend.routes.api.v1.discord.auth import auth_middleware
from backend.utils.config import BOT_TOKEN, FRONTEND_URI
from backend.utils.discord import exchange_code, get_auth_url, revoke_access_token
from backend.utils.discord.user import get_guild_member

router = APIRouter(prefix="/discord", tags=["discord"])


def users_by_bot_key_builder(
    func,
    namespace: str = "",
    *,
    request: Request = None,
    response: Response = None,
    **kwargs,
):
    return ":".join(
        [
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )


@router.get(
    "/users-by-bot/{user_id}",
    response_model=schemas.DiscordGuildMember,
    response_model_exclude_unset=True,
)
@cache(expire=600, key_builder=users_by_bot_key_builder)
async def get_user_by_bot(user_id: int | str):
    """
    Read Discord user by Discord id. Request to Discord is sent from bot.
    :param user_id: Discord user id
    :return: Discord user
    """
    return await get_guild_member("Bot", BOT_TOKEN, user_id)


@router.get(
    "/users/@me",
    response_model=schemas.DiscordGuildMember,
)
async def get_self(
    discord_user: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
):
    """
    Get data from self Discord account and Magatamy guild.
    """
    return discord_user


@router.get("/login")
def login_to_discord() -> Response:
    """
    Login to Discord.
    """
    return RedirectResponse(get_auth_url())


@router.get("/logout")
def logout(request: Request):
    """
    Logout from Discord.
    """
    response = RedirectResponse(FRONTEND_URI)

    cookies = request.cookies
    if access_token := cookies.get("access_token"):
        revoke_access_token(access_token)

    for cookie in cookies:
        response.delete_cookie(cookie, httponly=True)

    return response


@router.get("/callback")
async def get_auth_callback(
    code: str,
    request: Request,
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

    try:
        await auth_middleware(request, db)
    except HTTPException:
        pass

    expires = cookies.pop("expires_in")

    resp = RedirectResponse(FRONTEND_URI)

    for cookie in cookies.keys():
        resp.set_cookie(
            cookie, cookies.get(cookie), expires=expires, httponly=True, path="/"
        )

    return resp
