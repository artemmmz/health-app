import pytest

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.models import BaseModel
from tests.app import settings


@pytest.fixture(scope='class')
async def engine(settings) -> AsyncEngine:  # type: ignore
    """Create and return an AsyncEngine."""
    async_engine = create_async_engine(
        settings.POSTGRES_URL, future=True, echo=True
    )
    yield async_engine
    await async_engine.dispose(True)


@pytest.fixture(scope='function')
async def init_db(engine):
    """Create and drop tables."""
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture(scope='class')
async def session_factory(engine):
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    yield async_session


@pytest.fixture(scope='function')
async def session(init_db, session_factory) -> AsyncSession:  # type: ignore
    """Create and return an AsyncSession."""
    session: AsyncSession = session_factory()
    yield session

    await session.rollback()
    await session.close()
