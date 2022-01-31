import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import User
from app.schemas import UserCreate

data_in_db = {1: 100, 2: 200}

data_for_create = [
    UserCreate(id=1, amount=100),
    UserCreate(id=2, amount=200),
]

data_for_update = [
    (User(id=1, balance=100), 100),
    (User(id=2, balance=200), 200),
]


data_for_transfer = [
    (User(id=1, balance=100), User(id=2, balance=200), 100),
    (User(id=2, balance=200), User(id=1, balance=100), 200),
]


@pytest.mark.parametrize("user_id", [1, 2])
async def test_get(db_with_data: AsyncSession, user_id: int):
    user = await crud.user.get(db=db_with_data, user_id=user_id)
    assert user.id == user_id
    assert user.balance == data_in_db[user_id]


@pytest.mark.parametrize("user", data_for_create)
async def test_create(db: AsyncSession, user: UserCreate):
    new_user = await crud.user.create(db=db, request=user)
    assert new_user.id == user.id
    assert new_user.balance == user.amount


@pytest.mark.parametrize("user, amount", data_for_update)
async def test_update(db: AsyncSession, user: User, amount: int):
    old_balance = user.balance
    await crud.user.update(db=db, user=user, amount=amount)
    assert user.balance == old_balance + amount


@pytest.mark.parametrize("sender, receiver, amount", data_for_transfer)
async def test_transfer(db: AsyncSession, sender: User, receiver: User, amount: int):
    sender_old_balance = sender.balance
    receiver_old_balance = receiver.balance

    await crud.user.transfer(db=db, sender=sender, receiver=receiver, amount=amount)

    assert sender.balance == sender_old_balance - amount
    assert receiver.balance == receiver_old_balance + amount
