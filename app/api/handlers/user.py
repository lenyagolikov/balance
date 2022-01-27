from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import User, UserRequest

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def get_info(user_id: int, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
    return user


@router.post("/deposit", response_model=User)
async def deposit(request: UserRequest, response: Response, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, request.user_id)
    if not user:
        response.status_code = status.HTTP_201_CREATED
        return crud.user.create(db, request)
    return crud.user.update(db, request.value, user)


@router.post("/withdraw", response_model=User)
async def withdraw(request: UserRequest, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, request.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if request.value > user.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not enough money")

    return crud.user.update(db, -request.value, user)
