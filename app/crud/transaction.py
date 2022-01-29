from sqlalchemy.orm import Session

from app.models import Transaction


def get(db: Session, user_id: int) -> list[Transaction]:
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()
