from sqlalchemy import (
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.db.base import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    at_created = Column(DateTime(timezone=True), server_default=func.now())
