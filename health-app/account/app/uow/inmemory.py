from abc import ABC
from typing import Callable

from redis import Redis

from app.repositories import BlacklistTokenRepository
from app.repositories.redis import IBlacklistRepository
from app.uow.base import IUnitOfWork


class IInMemoryUnitOfWork(IUnitOfWork, ABC):
    """Interface for in-memory unit of-work."""
    blacklist_token_repository: IBlacklistRepository


class RedisUOW(IInMemoryUnitOfWork, ABC):
    """Redis unit of-work."""

    def __init__(self, connection_factory: Callable[[], Redis]):
        self.connection_factory = connection_factory

        self._connection: Redis | None = None

    def __aenter__(self) -> IInMemoryUnitOfWork:
        self._connection = self.connection_factory()

        self.blacklist_token_repository = BlacklistTokenRepository(self._connection)
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        self._connection = None

    def commit(self):
        ...

    def rollback(self):
        ...
