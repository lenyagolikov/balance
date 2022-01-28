import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models.user import User
from app.schemas import UserRequest


data_for_create = [
    UserRequest(id=1, amount=100),
    UserRequest(id=2, amount=200),
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
def test_get(db: Session, prepare_db, users_in_db: dict, user_id: int):
    user = crud.user.get(db=db, user_id=user_id)
    assert user.id == user_id
    assert user.balance == users_in_db[user_id]


@pytest.mark.parametrize("user", data_for_create)
def test_create(db: Session, prepare_db, user: UserRequest):
    new_user = crud.user.create(db=db, request=user)
    assert new_user.id == user.id
    assert new_user.balance == user.amount


@pytest.mark.parametrize("user, amount", data_for_update)
def test_update(db: Session, prepare_db, user: User, amount: int):
    old_balance = user.balance
    crud.user.update(db=db, user=user, amount=amount)
    assert user.balance == old_balance + amount


@pytest.mark.parametrize("sender, receiver, amount", data_for_transfer)
def transfer(db: Session, prepare_db, sender: User, receiver: User, amount: int):
    sender_old_balance = sender.balance
    receiver_old_balance = receiver.balance

    crud.user.transfer(db=db, sender=sender, receiver=receiver, amount=amount)

    assert sender.balance == sender_old_balance - amount
    assert receiver.balance == receiver_old_balance + amount
