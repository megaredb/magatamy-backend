from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@api_router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api_router.get("/shop", response_class=HTMLResponse)
async def shop_page(request: Request):
    return templates.TemplateResponse("shop.html", {"request": request})


@api_router.get("/social", response_class=HTMLResponse)
async def social_page(request: Request):
    return templates.TemplateResponse("social.html", {"request": request})
