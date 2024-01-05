from contextlib import asynccontextmanager
from os import environ
from dotenv import load_dotenv
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

load_dotenv(".env" if not environ.get("DEV") else ".env.dev")

from fastapi import FastAPI  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402
from routes import api, misc  # noqa: E402

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.api_router)
app.include_router(misc.api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
