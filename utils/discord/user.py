from json import JSONDecodeError

from async_lru import alru_cache
from fastapi import HTTPException
from httpx import HTTPStatusError, AsyncClient, Response

from schemas import DiscordUser
from schemas.discord import DiscordGuildMember
from utils import config
from utils.config import (
    DISCORD_API_ENDPOINT,
    DISCORD_GUILD_ID,
)


@alru_cache(maxsize=1024, typed=True, ttl=60)
async def get_user(
    token_type: str, access_token: str, user_id: str | int = "@me"
) -> DiscordUser:
    try:
        response: Response
        client: AsyncClient

        async with AsyncClient() as client:
            response = await client.get(
                f"{DISCORD_API_ENDPOINT}/users/{user_id}",
                headers={"Authorization": f"{token_type} {access_token}"},
            )

        response.raise_for_status()

        return DiscordUser.model_validate_json(response.text)

    except (JSONDecodeError, UnicodeDecodeError, ValueError):
        raise HTTPException(status_code=502, detail="Discord response decoding error.")

    except HTTPStatusError as err:
        resp_json: dict | str
        # Fix it later.
        try:
            resp_json = err.response.json()
        except JSONDecodeError:
            resp_json = err.response.text

        raise HTTPException(err.response.status_code, detail=resp_json)


@alru_cache(maxsize=1024, typed=True, ttl=60)
async def get_guild_member(
    token_type: str,
    access_token: str,
    user_id: str | int = "@me",
    guild_id: str | int = DISCORD_GUILD_ID,
) -> DiscordGuildMember:
    try:
        request_path = f"/users/{user_id}/guilds/{guild_id}/member"

        if token_type == "Bot":
            request_path = f"/guilds/{guild_id}/members/{user_id}"

        response: Response
        client: AsyncClient

        async with AsyncClient() as client:
            response = await client.get(
                f"{DISCORD_API_ENDPOINT}{request_path}",
                headers={"Authorization": f"{token_type} {access_token}"},
            )

        response.raise_for_status()

        guild_member = DiscordGuildMember.model_validate_json(response.text)

        if not guild_member.nick:
            guild_member.nick = guild_member.user.global_name
        if not guild_member.avatar:
            guild_member.avatar = guild_member.user.avatar

        return guild_member

    except (JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=502, detail="Discord response decoding error.")

    except HTTPStatusError as err:
        resp_json: dict | str
        # Fix it later.
        try:
            resp_json = err.response.json()
        except JSONDecodeError:
            resp_json = err.response.text

        raise HTTPException(err.response.status_code, detail=resp_json)


async def create_dm(user_id: str | int) -> Response:
    client: AsyncClient

    async with AsyncClient() as client:
        response = await client.post(
            f"{DISCORD_API_ENDPOINT}/users/@me/channels",
            headers={"Authorization": f"Bot {config.BOT_TOKEN}"},
            json={"recipient_id": str(user_id)},
        )

        return response


async def send_message(user_id: str | int, content: str) -> Response | None:
    response: Response
    client: AsyncClient

    dm_response = await create_dm(user_id)

    if dm_response.status_code != 200:
        return

    async with AsyncClient() as client:
        response = await client.post(
            f"{DISCORD_API_ENDPOINT}/channels/{dm_response.json().get('id')}/messages",
            headers={"Authorization": f"Bot {config.BOT_TOKEN}"},
            data={"content": content},
        )

        return response
