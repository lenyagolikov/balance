import asyncio
import os
from typing import AsyncGenerator, Callable, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_engine, async_session
from app.models import Base, User


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
async def db() -> AsyncSession:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with async_session(bind=conn) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
async def db_with_data(db: AsyncSession) -> AsyncSession:
    user1 = User(id=1, balance=100)
    user2 = User(id=2, balance=200)
    db.add_all([user1, user2])
    await db.commit()
    return db


@pytest.fixture
def override_get_db(db: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db

    return _override_get_db


@pytest.fixture
def app(override_get_db: Callable) -> FastAPI:
    from app.api.deps import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url=f"http://{os.getenv('HOST')}:{os.getenv('PORT')}"
    ) as ac:
        yield ac
