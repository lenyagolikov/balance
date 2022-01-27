from sqlalchemy import Column, DECIMAL, Integer

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    balance = Column(DECIMAL, nullable=False)
