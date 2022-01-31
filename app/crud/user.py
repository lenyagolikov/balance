from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Transaction, User
from app.schemas import UserCreate


async def get(db: AsyncSession, user_id: int) -> User:
    stmt = select(User).options(selectinload(User.transactions))
    user = await db.execute(stmt.where(User.id == user_id))
    return user.scalar()


async def create(db: AsyncSession, request: UserCreate) -> User:
    user = User(id=request.id, balance=request.amount)
    transaction = Transaction(user_id=user, type="deposit", amount=request.amount)
    user.transactions.append(transaction)

    db.add(user)
    await db.commit()

    return user


async def update(db: AsyncSession, user: User, amount: int) -> User:
    if amount > 0:
        transaction = Transaction(user_id=user, type="deposit", amount=amount)
    else:
        transaction = Transaction(user_id=user, type="withdraw", amount=amount)

    user.balance += amount
    user.transactions.append(transaction)

    db.add(user)
    await db.commit()

    return user


async def transfer(db: AsyncSession, sender: User, receiver: User, amount: int):
    sender_transaction = Transaction(user_id=sender, type="transfer", amount=-amount)
    receiver_transaction = Transaction(user_id=receiver, type="transfer", amount=amount)

    sender.balance -= amount
    receiver.balance += amount

    sender.transactions.append(sender_transaction)
    receiver.transactions.append(receiver_transaction)

    db.add_all([sender, receiver])
    await db.commit()
