from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import Transaction

router = APIRouter()


@router.get("/{user_id}", response_model=list[Transaction])
def get_transactions(
    user_id: int, limit: int = 5, offset: int = 1, db: Session = Depends(deps.get_db)
):
    transactions = crud.transaction.get(
        db=db, user_id=user_id, limit=limit, offset=offset
    )
    return transactions
