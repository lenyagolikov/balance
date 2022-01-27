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
    db.refresh(user)
    return user


def deposit(db: Session, request: UserRequest, user: User) -> User:
    user.balance += request.value
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def withdraw(db: Session, request: UserRequest, user: User) -> User | None:
    if request.value > user.balance:
        return
    user.balance -= request.value
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
