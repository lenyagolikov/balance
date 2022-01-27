from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserRequest


def get(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


def create(db: Session, request: UserRequest) -> User:
    user = User(user_id=request.user_id, balance=request.value)
    db.add(user)
    db.commit()
    return user


def update(db: Session, user: User, value: int) -> User:
    user.balance += value
    db.add(user)
    db.commit()
    return user


def transfer(db: Session, sender: User, receiver: User, value: int):
    sender.balance -= value
    receiver.balance += value

    db.add_all([sender, receiver])
    db.commit()
