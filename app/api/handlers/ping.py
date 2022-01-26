from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()


@router.get("/app")
def ping_app():
    return {"message": "ok"}


@router.get("/db")
def ping_db(db: Session = Depends(deps.get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return {"message": "pg is down"}
    return {"message": "ps is up"}
