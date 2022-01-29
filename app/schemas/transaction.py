from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Transaction(BaseModel):
    user_id: int
    type: str
    amount: Decimal
    at_created: datetime

    class Config:
        orm_mode = True
