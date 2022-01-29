from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    user_id: int
    type: str
    amount: Decimal = Field(gt=0)
    at_created: datetime

    class Config:
        use_enum_values = True
        orm_mode = True
