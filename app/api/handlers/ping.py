from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()


@router.get("/app")
def ping_app():
    return {"detail": "app is up"}


@router.get("/db")
def ping_db(response: Response, db: Session = Depends(deps.get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"detail": "db is down"}
    return {"detail": "db is up"}
