from app.db.base import Base
from app.db.session import engine

from app.models.user import User  # noqa

Base.metadata.create_all(bind=engine)
