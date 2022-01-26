from decimal import Decimal
from pydantic import BaseModel


class UserBase(BaseModel):
    balance: Decimal


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass
