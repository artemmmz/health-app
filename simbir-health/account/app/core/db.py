from app.core.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import Generator

engine = create_async_engine(
    settings.POSTGRES_URL,
    future=True,
    echo=True,
    execution_option={'isolation_level': 'AUTOCOMMIT'}
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> Generator[AsyncSession]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
