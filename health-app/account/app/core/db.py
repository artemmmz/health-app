"""Database module."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_async_engine(settings.POSTGRES_URL, future=True, echo=True)

async_session = sessionmaker(  # type: ignore
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with async_session() as session:
        return session
