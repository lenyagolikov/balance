from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps


async def test_get_db_deps():
    async_session = await deps.get_db().__anext__()
    assert isinstance(async_session, AsyncSession)
