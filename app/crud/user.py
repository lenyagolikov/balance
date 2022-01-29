from datetime import datetime
from sqlalchemy.orm import Session

from app.models import User, Transaction
from app.schemas import UserCreate


def get(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def create(db: Session, request: UserCreate) -> User:
    user = User(id=request.id, balance=request.amount)
    transaction = Transaction(
        user_id=user,
        type="deposit",
        amount=request.amount,
        at_created=datetime.utcnow(),
    )
    user.transactions.append(transaction)

    db.add(user)
    db.commit()

    return user


def update(db: Session, user: User, amount: int) -> User:
    if amount > 0:
        transaction = Transaction(
            user_id=user, type="deposit", amount=amount, at_created=datetime.utcnow()
        )
    else:
        transaction = Transaction(
            user_id=user, type="withdraw", amount=amount, at_created=datetime.utcnow()
        )

    user.balance += amount
    user.transactions.append(transaction)

    db.add(user)
    db.commit()

    return user


def transfer(db: Session, sender: User, receiver: User, amount: int):
    current_time = datetime.utcnow()

    sender_transaction = Transaction(
        user_id=sender, type="transfer", amount=-amount, at_created=current_time
    )
    receiver_transaction = Transaction(
        user_id=receiver, type="transfer", amount=amount, at_created=current_time
    )

    sender.balance -= amount
    receiver.balance += amount

    sender.transactions.append(sender_transaction)
    receiver.transactions.append(receiver_transaction)

    db.add_all([sender, receiver])
    db.commit()
