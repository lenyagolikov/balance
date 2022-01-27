from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import User, UserRequest

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def get_info(user_id: int, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="user not found")
    return user


@router.post("/deposit", response_model=User)
async def deposit(request: UserRequest, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, request.user_id)
    if not user:
        return crud.user.create(db, request)
    return crud.user.deposit(db, request, user)


@router.post("/withdraw", response_model=User)
async def withdraw(request: UserRequest, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, request.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="user not found")

    result = crud.user.withdraw(db, request, user)
    if not result:
        raise HTTPException(status_code=400, detail="not enough money")
    return user
