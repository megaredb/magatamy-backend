from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from routes.api import deps
from routes.api.v1.discord import auth_middleware

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


def prepare_request_for_template(resp_dict: dict, db: Session) -> dict:
    result = resp_dict
    request: Request = resp_dict.get("request")

    authorized = False

    if user := auth_middleware(request, db):
        authorized = True

        result.update(
            {
                "avatar_url": (
                    f"https://cdn.discordapp.com/avatars/"
                    f"{user.get('id')}/{user.get('avatar')}.webp?size=64"
                ),
                "username": user.get('username')
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
        "index.html", prepare_request_for_template({"request": request}, db)
    )

@api_router.get("/servers", response_class=HTMLResponse)
async def shop_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "servers.html", prepare_request_for_template({"request": request}, db)
    )

@api_router.get("/social", response_class=HTMLResponse)
async def social_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "social.html", prepare_request_for_template({"request": request}, db)
    )

@api_router.get("/shop", response_class=HTMLResponse)
async def social_page(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    return templates.TemplateResponse(
        "shop.html", prepare_request_for_template({"request": request}, db)
    )
