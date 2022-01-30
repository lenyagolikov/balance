from sqlalchemy.orm import Session

from app.models import Transaction


def get(db: Session, user_id: int, limit: int, offset: int) -> list[Transaction]:
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.at_created.desc())
        .all()
    )
    return transactions[offset - 1 : offset + limit - 1]
