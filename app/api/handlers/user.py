from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import User, UserRequest, UserTransferRequest, UserTransferResponse
from app.utils.currency import transfer_to_EUR, transfer_to_USD

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def get_info(
    user_id: int, currency: str = "RUB", db: Session = Depends(deps.get_db)
):
    user = crud.user.get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )

    match currency:
        case "USD":
            user.balance = transfer_to_USD(user.balance)
        case "EUR":
            user.balance = transfer_to_EUR(user.balance)

    return user


@router.post("/deposit", response_model=User)
async def deposit(
    request: UserRequest, response: Response, db: Session = Depends(deps.get_db)
):
    user = crud.user.get(db=db, user_id=request.id)
    if not user:
        response.status_code = status.HTTP_201_CREATED
        return crud.user.create(db=db, request=request)
    return crud.user.update(db=db, user=user, amount=request.amount)


@router.post("/withdraw", response_model=User)
async def withdraw(request: UserRequest, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db=db, user_id=request.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )

    if request.amount > user.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="not enough money"
        )

    return crud.user.update(db=db, user=user, amount=-request.amount)


@router.post("/transfer", response_model=UserTransferResponse)
async def transfer(request: UserTransferRequest, db: Session = Depends(deps.get_db)):
    sender = crud.user.get(db=db, user_id=request.from_)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="sender not found"
        )

    if request.amount > sender.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="not enough money"
        )

    receiver = crud.user.get(db=db, user_id=request.to)
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="receiver not found"
        )

    crud.user.transfer(db=db, sender=sender, receiver=receiver, amount=request.amount)

    return {"detail": "Success"}
