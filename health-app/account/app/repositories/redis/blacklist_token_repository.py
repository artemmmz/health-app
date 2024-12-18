import datetime
import uuid
from abc import ABC, abstractmethod
from typing import Optional

from app.repositories.redis.base import RedisRepository
from app.repositories.sqlalchemy.base import AbstractRepository


class IBlacklistRepository(AbstractRepository, ABC):
    """Interface for blacklist repository."""

    @abstractmethod
    async def add_token(
        self,
        token_uuid: str | uuid.UUID,
        expires_in: Optional[datetime.timedelta] = None,
        expires_at: Optional[datetime.datetime] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def exists_token(self, token_uuid: str | uuid.UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove_token(self, token_uuid: str | uuid.UUID) -> bool:
        raise NotImplementedError

    async def get_all_tokens(
        self, offset: int = 0, limit: int = 100
    ) -> list[dict[str, str]]:
        raise NotImplementedError


class BlacklistTokenRepository(IBlacklistRepository, RedisRepository, ABC):
    """Repository for blacklist tokens."""

    prefix = 'ms-accounts:blacklist-tokens'
    default_value = 'blacklisted'

    @classmethod
    def __get_key(cls, name: str) -> str:
        return f'{cls.prefix}:{name}'

    async def add_token(
        self,
        token_uuid: str | uuid.UUID,
        expires_in: Optional[int | datetime.timedelta] = None,
        expires_at: Optional[int | datetime.datetime] = None,
    ) -> None:
        """Add token to blacklist."""
        token_uuid = str(token_uuid)
        return await self.connection.set(
            self.__get_key(token_uuid),
            self.default_value,
            ex=expires_in,
            exat=expires_at,
        )

    async def exists_token(self, token_uuid: str | uuid.UUID) -> bool:
        """Check if token exists."""
        token_uuid = str(token_uuid)
        result = await self.connection.get(self.__get_key(token_uuid))
        return (
            result is not None and result.decode('ascii') == self.default_value
        )

    async def remove_token(self, token_uuid: str | uuid.UUID) -> None:
        """Remove token from blacklist."""
        return await self.connection.set(
            self.__get_key(token_uuid), 'revoked', keepttl=True
        )

    async def get_all_tokens(
        self, offset: int = 0, limit: int = 100
    ) -> list[dict[str, str]]:
        """Get all blacklisted tokens."""
        return await self.connection.scan(
            offset, self.__get_key('*'), limit, _type='STRING'
        )
