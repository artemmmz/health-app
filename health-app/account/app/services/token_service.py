import datetime
from typing import Optional
from uuid import UUID

from app.uow.inmemory import IInMemoryUnitOfWork


class TokenService:
    """Service for working with tokens."""

    @staticmethod
    async def blacklist_token(
        uow: IInMemoryUnitOfWork,
        token_uuid: UUID | str,
        expires_in: Optional[datetime.timedelta | int] = None,
        expires_at: Optional[datetime.datetime | int] = None,
    ):
        async with uow:
            return await uow.blacklist_token_repository.add_token(
                token_uuid, expires_in=expires_in, expires_at=expires_at
            )

    @staticmethod
    async def check_blacklist_token(
        uow: IInMemoryUnitOfWork, token_uuid: UUID | str
    ) -> bool:
        async with uow:
            return await uow.blacklist_token_repository.exists_token(
                token_uuid
            )

    @staticmethod
    async def get_all_blocked_tokens(
        uow: IInMemoryUnitOfWork, offset: int = 0, limit: int = 100
    ):
        async with uow:
            return await uow.blacklist_token_repository.get_all_tokens(
                offset=offset, limit=limit
            )

    @staticmethod
    async def revoke_token(uow: IInMemoryUnitOfWork, token_uuid: UUID | str):
        async with uow:
            return await uow.blacklist_token_repository.remove_token(
                token_uuid
            )
