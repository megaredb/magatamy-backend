from json import JSONDecodeError

from async_lru import alru_cache
from fastapi import HTTPException
from httpx import HTTPStatusError, AsyncClient, Response

import schemas
from models import Ticket
from schemas import DiscordUser
from schemas.discord import DiscordGuildMember, CreateDiscordMessage
from utils import config
from utils.config import (
    DISCORD_API_ENDPOINT,
    DISCORD_GUILD_ID,
)
from utils.discord import ROLE_FROM_SERVER
from utils.minecraft import ServerEnum
from utils.ticket import TicketStatus


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
            if not guild_member.nick:
                guild_member.nick = guild_member.user.username
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


async def send_message(
    channel_id: str | int, msg: CreateDiscordMessage, is_dm: bool = True
) -> Response | None:
    response: Response
    client: AsyncClient

    if is_dm:
        dm_response = await create_dm(channel_id)

        if dm_response.status_code != 200:
            return

        channel_id = dm_response.json().get("id")

    msg_data = msg.model_dump(mode="json", exclude_unset=True, exclude_none=True)

    async with AsyncClient() as client:
        response = await client.post(
            f"{DISCORD_API_ENDPOINT}/channels/{channel_id}/messages",
            headers={"Authorization": f"Bot {config.BOT_TOKEN}"},
            json=msg_data,
        )

        return response


async def give_role(guild_id: str, user_id: str, role_id: str) -> Response | None:
    async with AsyncClient() as client:
        response = await client.put(
            f"{DISCORD_API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers={"Authorization": f"Bot {config.BOT_TOKEN}"},
        )

        return response


async def send_ticket_update(
    ticket: Ticket, ticket_in: schemas.TicketUpdate, updated_by: DiscordGuildMember
):
    statuses = {
        TicketStatus.OPEN: "открыта",
        TicketStatus.CLOSED: "отклонена",
        TicketStatus.ACCEPTED: "принята",
    }

    msg = schemas.discord.CreateDiscordMessage()

    msg.embeds = [
        {
            "title": "Добро пожаловать на Второй сезон! :slight_smile:",
            "description": "Приветствуем тебя в нашем втором сезоне. Вот несколько полезных ссылок для начала:",
            "fields": [
                {"name": "Айпи сервера", "value": "plus.magatamy.com"},
                {
                    "name": "Онлайн карта 2-го сезона",
                    "value": "[Ссылка](http://host-plus.magatamy.com:25582/)",
                },
                {
                    "name": "Вики",
                    "value": "[Ссылка на вики](https://magatamy-1.gitbook.io/magatamy)",
                },
                {
                    "name": "Наш Дискрд",
                    "value": "[magatamy](https://discord.gg/TntRVqWGHk)",
                },
                {
                    "name": "Наш сайт",
                    "value": "[magatamy.com](https://magatamy.com/)",
                },
            ],
            "footer": {"text": "Спасибо за присоединение! Удачи в новом сезоне."},
            "image": {
                "url": (
                    "https://media.discordapp.net/attachments/1163167620992860371/"
                    "1199438645065678968/vanilla_plus_16.png"
                )
            },
        }
    ]

    prev_status = TicketStatus(ticket.status)
    status = ticket_in.status

    match ticket.form.extra_id:
        case "vanilla" if status == TicketStatus.ACCEPTED:
            msg.embeds[0]["fields"][0]["value"] = "mc.magatamy.com"
            msg.embeds[0]["fields"][1][
                "value"
            ] = "[Ссылка](http://host-mc.magatamy.com:25673/)"
            msg.embeds[0]["image"]["url"] = (
                "https://media.discordapp.net/attachments/1163167620992860371/"
                "1199438660584620222/vanilla_16.png"
            )

        case "vanilla-plus" if status == TicketStatus.ACCEPTED:
            pass

        case _:
            msg.embeds = []
            msg.attachments = []
            msg.content = (
                f"> **<@{ticket.author_id}>, "
                f'Ваша заявка "{ticket.form.name}" с ID {ticket.id} получила новый статус!**\n> \n'
                f"> Новый статус: *{statuses[status]}*."
            )

    log_msg = schemas.discord.CreateDiscordMessage()
    log_msg.embeds = [
        {
            "title": f"Обновление тикета с ID {ticket.id}",
            "description": (
                f"**Тикет обновлен пользователем <@{updated_by.user.id}>**\n"
                f"**Старый статус:** {statuses[prev_status]}\n"
                f"**Новый статус:** {statuses[status]}\n\n"
                f"**Форма тикета:** {ticket.form.name} (ID: {ticket.form_id})\n"
                f"**Автор тикета:** <@{ticket.author_id}>"
            ),
            "color": 5814783,
        }
    ]

    await send_message(config.DISCORD_LOG_CHANNEL_ID, log_msg, False)
    await send_message(ticket.author_id, msg)


async def send_roles_update(user_id: str, server: ServerEnum):
    await give_role(config.DISCORD_GUILD_ID, user_id, ROLE_FROM_SERVER[server])
