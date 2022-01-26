from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import User

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def get_balance(user_id: int, db: Session = Depends(deps.get_db)):
    user = await crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user
