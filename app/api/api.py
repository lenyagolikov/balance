from fastapi import APIRouter

from app.api.handlers import user, ping

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
