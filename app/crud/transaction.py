from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas import TransactionCreate


def get(db: Session, user_id: int) -> list[Transaction]:
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return transactions


def create(db: Session, request: TransactionCreate) -> Transaction:
    transaction = Transaction(**request)
    db.add(transaction)
    db.commit()
    return transaction
