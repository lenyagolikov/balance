from decimal import Decimal

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int


class UserInDB(UserBase):
    balance: Decimal = Field(ge=0)


class UserBalance(UserInDB):
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    amount: Decimal = Field(gt=0)


class UserTransferCreate(BaseModel):
    from_: int = Field(alias="from")
    to: int
    amount: Decimal = Field(gt=0)
