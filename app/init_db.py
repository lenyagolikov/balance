from app.db.session import engine
from app.models import Base, Transaction, User  # noqa

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
