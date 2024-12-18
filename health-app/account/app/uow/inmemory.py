from abc import ABC
from typing import Callable

from redis.asyncio import Redis

from app.core.redis import create_redis
from app.repositories import BlacklistTokenRepository
from app.repositories.redis import IBlacklistRepository
from app.uow.base import IUnitOfWork


class IInMemoryUnitOfWork(IUnitOfWork, ABC):
    """Interface for in-memory unit of-work."""

    blacklist_token_repository: IBlacklistRepository


class RedisUOW(IInMemoryUnitOfWork, ABC):
    """Redis unit of-work."""

    def __init__(self, connection_factory: Callable[[], Redis] = create_redis):
        self.connection_factory = connection_factory

        self._connection: Redis | None = None

    async def __aenter__(self) -> IInMemoryUnitOfWork:
        self._connection = self.connection_factory()

        self.blacklist_token_repository = BlacklistTokenRepository(
            self._connection
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._connection.close()
        self._connection = None

    async def commit(self) -> None:
        await self._connection.execute_command()

    async def rollback(self) -> None: ...
