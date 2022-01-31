import asyncio

from app.db.session import engine
from app.models import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def main():
    asyncio.run(init_db())


if __name__ == "__main__":
    main()
