from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories import UserRepository, RoleRepository
from app.repositories.sqlalchemy import IRoleRepository, IUserRepository
from app.uow.base import IUnitOfWork


class IDatabaseUnitOfWork(IUnitOfWork, ABC):
    """Interface for database unit of-work."""

    role_repository: IRoleRepository
    user_repository: IUserRepository


class SQLAlchemyUOW(IDatabaseUnitOfWork, ABC):
    """Unit-of-work for SQLModel and SQLAlchemy repositories."""

    def __init__(self, session_factory=get_db):
        self._session = None

        self.session_factory = session_factory

    async def __aenter__(self):
        self._session = await self.session_factory()

        self.user_repository = UserRepository(self.session)
        self.role_repository = RoleRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self._session.close()

        self._session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    @property
    def session(self) -> AsyncSession | None:
        return self._session
