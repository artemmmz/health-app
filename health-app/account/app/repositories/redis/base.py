import datetime
from abc import ABC
from typing import Literal, Optional

from redis.asyncio import Redis

from app.repositories.base import AbstractRepository
from app.utils.datetime import get_now


class IRedisRepository(AbstractRepository, ABC):
    """Interface for Redis repository."""

    ...


class RedisRepository(IRedisRepository, ABC):
    """Repository for Redis."""

    prefix: str

    def __init__(self, connection):
        self.__connection = connection

    @property
    def connection(self) -> Redis:
        return self.__connection

    async def get_one(self, key: str): ...  # GET with limit 1 and error

    async def get_all(
        self, offset: int = 0, limit: int = 100
    ): ...  # SCAN with limit

    async def add_one(
        self,
        key: str,
        value: str,
        expires_in: Optional[datetime.timedelta] = None,
        expires_at: Optional[datetime.datetime] = None,
    ):
        if isinstance(value, list):
            result = await self.connection.rpush(key, *value)
        elif isinstance(value, set):
            result = await self.connection.sadd(key, *value)
        elif isinstance(value, dict):
            result = await self.connection.hset(key, mapping=value)
        else:
            return await self.connection.set(
                key,
                value,
            )
        expire_secs = None
        if expires_in is not None:
            expire_secs = expires_in.total_seconds()
        elif expires_at is not None:
            expire_secs = (expires_at - get_now()).total_seconds()

        if expire_secs is not None:
            await self.connection.expire(key, expire_secs)
        return result

    async def update_one(
        self,
        key: str,
        value: str,
        operation: Literal['add', 'update', 'remove'] = 'update',
    ): ...
