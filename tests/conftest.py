import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.core.config import settings
from app.api.deps import get_db
from app.main import app
from app.models.user import User


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client(prepare_db):
    return TestClient(app)


@pytest.fixture()
def add_data_to_db():
    with Session() as session:
        for id in range(1, 3):
            user = User(user_id=id, balance=id * 100)
            session.add(user)
            session.commit()
