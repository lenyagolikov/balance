from decimal import Decimal

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    balance: Decimal

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    user_id: int
    value: Decimal = Field(gt=0)


class UserTransfer(BaseModel):
    from_: int = Field(alias="from")
    to: int
    value: Decimal = Field(gt=0)


class UserTransferResponse(BaseModel):
    detail: str
