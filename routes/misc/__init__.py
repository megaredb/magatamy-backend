from fastapi import APIRouter
from httpx import AsyncClient, URL
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")
map_client = AsyncClient(base_url="http://135.181.126.137:25636/")


@api_router.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def _map_reverse_proxy(request: Request):
    print(request.url.path)
    path = request.url.path[len("/map") :]
    print(path)
    url = URL(path=path, query=request.url.query.encode("utf-8"))
    rp_req = map_client.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body()
    )
    rp_resp = await map_client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )


api_router.add_route("/map/{path:path}", _map_reverse_proxy, ["GET", "POST"])
