from fastapi import APIRouter
from routes.api import v1

api_router = APIRouter(prefix="/api")
api_router.include_router(v1.api_router)
