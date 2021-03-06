from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.schemas import UserBalance, UserCreate, UserTransfer
from app.utils.currency import convert_to_EUR, convert_to_USD

router = APIRouter()


@router.get("/{user_id}", response_model=UserBalance)
async def get_balance(
    user_id: int, currency: str = "RUB", db: AsyncSession = Depends(deps.get_db)
):
    user = await crud.user.get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )

    match currency:
        case "USD":
            user.balance = convert_to_USD(user.balance)
        case "EUR":
            user.balance = convert_to_EUR(user.balance)

    return user


@router.post("/deposit", response_model=UserBalance)
async def deposit(
    request: UserCreate, response: Response, db: AsyncSession = Depends(deps.get_db)
):
    user = await crud.user.get(db=db, user_id=request.id)
    if not user:
        response.status_code = status.HTTP_201_CREATED
        return await crud.user.create(db=db, request=request)
    return await crud.user.update(db=db, user=user, amount=request.amount)


@router.post("/withdraw", response_model=UserBalance)
async def withdraw(request: UserCreate, db: AsyncSession = Depends(deps.get_db)):
    user = await crud.user.get(db=db, user_id=request.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )

    if request.amount > user.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="not enough money"
        )

    return await crud.user.update(db=db, user=user, amount=-request.amount)


@router.post("/transfer")
async def transfer(request: UserTransfer, db: AsyncSession = Depends(deps.get_db)):
    sender = await crud.user.get(db=db, user_id=request.from_)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="sender not found"
        )

    if request.amount > sender.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="not enough money"
        )

    receiver = await crud.user.get(db=db, user_id=request.to)
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="receiver not found"
        )

    await crud.user.transfer(
        db=db, sender=sender, receiver=receiver, amount=request.amount
    )

    return {"detail": "Success"}
