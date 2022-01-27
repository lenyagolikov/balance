from decimal import Decimal

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_id: int


class UserInDB(UserBase):
    balance: Decimal


class User(UserInDB):
    class Config:
        orm_mode = True


class UserRequest(UserBase):
    value: Decimal = Field(gt=0)
