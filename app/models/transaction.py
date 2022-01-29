from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    DECIMAL,
    Enum as DbEnum,
    ForeignKey,
    Integer,
    String,
)

from app.db.base import Base


class Type(Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    transfer = "transfer"


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String, DbEnum(Type), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    at_created = Column(DateTime, default=datetime.utcnow())
