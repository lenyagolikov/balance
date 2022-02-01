from typing import Generator

from app.db.session import async_session


async def get_db() -> Generator:
    async with async_session() as session:
        yield session
