from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.routes import api, misc
from backend.utils.config import FRONTEND_URI

tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
    {
        "name": "discord",
        "description": "Operations with discord.",
    },
    {
        "name": "minecraft",
        "description": "Operations with minecraft (WebGate plugin).",
    },
    {
        "name": "tickets",
        "description": "Operations with tickets.",
    },
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(openapi_tags=tags_metadata, lifespan=lifespan)

origins = [FRONTEND_URI]

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.api_router)
app.include_router(misc.api_router)
