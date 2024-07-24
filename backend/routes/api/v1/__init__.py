from fastapi import APIRouter
from backend.routes.api.v1 import product, discord, ticket, minecraft, payment, promo

api_router = APIRouter(prefix="/v1")
api_router.include_router(product.router)
api_router.include_router(discord.router)
api_router.include_router(minecraft.router)
api_router.include_router(ticket.router)
api_router.include_router(payment.router)
api_router.include_router(promo.router)
