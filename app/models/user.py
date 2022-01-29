from sqlalchemy import Column, DECIMAL, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    balance = Column(DECIMAL, nullable=False)
    transactions = relationship(
        "Transaction", backref="user", cascade="all, delete", passive_deletes=True
    )
