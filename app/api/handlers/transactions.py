from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.schemas import Transaction

router = APIRouter()


@router.get("/{user_id}", response_model=list[Transaction])
async def get_transactions(
    user_id: int,
    limit: int = 5,
    offset: int = 1,
    db: AsyncSession = Depends(deps.get_db),
):
    transactions = await crud.transaction.get(
        db=db, user_id=user_id, limit=limit, offset=offset
    )
    return transactions
