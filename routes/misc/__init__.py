from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from routes.api import deps
from routes.api.v1.discord import auth_middleware
from routes.api.v1.discord.auth import only_moderator
from schemas import DiscordGuildMember

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def prepare_request_for_template(resp_dict: dict, db: Session) -> dict:
    result = resp_dict
    request: Request = resp_dict.get("request")

    authorized = False

    try:
        guild_member = await auth_middleware(request, db)
    except HTTPException:
        guild_member = None

    if guild_member:
        authorized = True

        result.update(
            {
                "avatar_url": (
                    f"https://cdn.discordapp.com/avatars/"
                    f"{guild_member.user.id}/{guild_member.avatar}.webp?size=64"
                ),
                "username": guild_member.nick,
            }
        )

    result.update({"authorized": authorized})

    return result


@api_router.get("/", response_class=HTMLResponse)
async def main_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "index.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/servers", response_class=HTMLResponse)
async def servers_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "servers.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/social", response_class=HTMLResponse)
async def social_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "social.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/shop", response_class=HTMLResponse)
async def shop_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "shop.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/admin", response_class=HTMLResponse)
async def admin_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[DiscordGuildMember, Depends(only_moderator)],
):
    return templates.TemplateResponse(
        "admin.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/agreement", response_class=HTMLResponse)
async def agreement_page(
    request: Request, db: Annotated[Session, Depends(deps.get_db)]
):
    return templates.TemplateResponse(
        "agreement.html", await prepare_request_for_template({"request": request}, db)
    )


@api_router.get("/policy", response_class=HTMLResponse)
async def policy_page(request: Request, db: Annotated[Session, Depends(deps.get_db)]):
    return templates.TemplateResponse(
        "policy.html", await prepare_request_for_template({"request": request}, db)
    )
