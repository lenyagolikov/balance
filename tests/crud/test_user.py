import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models.user import User
from app.schemas import UserRequest


data_for_create = [
    UserRequest(user_id=1, value=100),
    UserRequest(user_id=2, value=200),
]

data_for_update = [
    (User(user_id=1, balance=100), 100),
    (User(user_id=2, balance=200), 200),
]


data_for_transfer = [
    (User(user_id=1, balance=100), User(user_id=2, balance=200), 100),
    (User(user_id=2, balance=200), User(user_id=1, balance=100), 200),
]


@pytest.mark.parametrize("user_id", [1, 2])
def test_get(db: Session, prepare_db, users_in_db: dict, user_id: int):
    user = crud.user.get(db=db, user_id=user_id)
    assert user.user_id == user_id
    assert user.balance == users_in_db[user_id]


@pytest.mark.parametrize("user", data_for_create)
def test_create(db: Session, prepare_db, user: UserRequest):
    new_user = crud.user.create(db=db, request=user)
    assert new_user.user_id == user.user_id
    assert new_user.balance == user.value


@pytest.mark.parametrize("user, value", data_for_update)
def test_update(db: Session, prepare_db, user: User, value: int):
    old_balance = user.balance
    crud.user.update(db=db, user=user, value=value)
    assert user.balance == old_balance + value


@pytest.mark.parametrize("sender, receiver, value", data_for_transfer)
def transfer(db: Session, prepare_db, sender: User, receiver: User, value: int):
    sender_old_balance = sender.balance
    receiver_old_balance = receiver.balance

    crud.user.transfer(db=db, sender=sender, receiver=receiver, value=value)

    assert sender.balance == sender_old_balance - value
    assert receiver.balance == receiver_old_balance + value
