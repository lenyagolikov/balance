from fastapi import APIRouter

from app.api.handlers import ping, transactions, users

api_router = APIRouter()

api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
