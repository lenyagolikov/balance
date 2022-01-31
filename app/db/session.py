from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
