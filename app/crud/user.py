from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserRequest


def get(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def create(db: Session, request: UserRequest) -> User:
    user = User(id=request.id, balance=request.amount)
    db.add(user)
    db.commit()
    return user


def update(db: Session, user: User, amount: int) -> User:
    user.balance += amount
    db.add(user)
    db.commit()
    return user


def transfer(db: Session, sender: User, receiver: User, amount: int):
    sender.balance -= amount
    receiver.balance += amount

    db.add_all([sender, receiver])
    db.commit()
