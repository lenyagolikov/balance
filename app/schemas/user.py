from decimal import Decimal

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    balance: Decimal

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    id: int
    amount: Decimal = Field(gt=0)


class UserTransferRequest(BaseModel):
    from_: int = Field(alias="from")
    to: int
    amount: Decimal = Field(gt=0)


class UserTransferResponse(BaseModel):
    detail: str
