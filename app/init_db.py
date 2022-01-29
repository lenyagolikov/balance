from app.db.base import Base
from app.db.session import engine

from app.models.user import User  # noqa
from app.models.transaction import Transaction  # noqa


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
