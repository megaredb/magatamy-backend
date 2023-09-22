from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@api_router.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
