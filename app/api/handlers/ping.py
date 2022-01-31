from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps

router = APIRouter()


@router.get("/app")
async def ping_app():
    return {"detail": "app is up"}


@router.get("/db")
async def ping_db(response: Response, db: AsyncSession = Depends(deps.get_db)):
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"detail": "db is down"}
    return {"detail": "db is up"}
