from fastapi import APIRouter
from routes.api.v1 import product, discord

api_router = APIRouter(prefix="/v1")
api_router.include_router(product.router)
api_router.include_router(discord.router)
