from sqlalchemy.orm import Session

from app.models import Transaction, User
from app.schemas import UserCreate


def get(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def create(db: Session, request: UserCreate) -> User:
    user = User(id=request.id, balance=request.amount)
    transaction = Transaction(user_id=user, type="deposit", amount=request.amount)
    user.transactions.append(transaction)

    db.add(user)
    db.commit()

    return user


def update(db: Session, user: User, amount: int) -> User:
    if amount > 0:
        transaction = Transaction(user_id=user, type="deposit", amount=amount)
    else:
        transaction = Transaction(user_id=user, type="withdraw", amount=amount)

    user.balance += amount
    user.transactions.append(transaction)

    db.add(user)
    db.commit()

    return user


def transfer(db: Session, sender: User, receiver: User, amount: int):
    sender_transaction = Transaction(user_id=sender, type="transfer", amount=-amount)
    receiver_transaction = Transaction(user_id=receiver, type="transfer", amount=amount)

    sender.balance -= amount
    receiver.balance += amount

    sender.transactions.append(sender_transaction)
    receiver.transactions.append(receiver_transaction)

    db.add_all([sender, receiver])
    db.commit()
