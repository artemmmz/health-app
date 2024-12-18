from uuid import UUID

from app.utils.uow import IUnitOfWork


class BlacklistTokenService:
    @staticmethod
    async def add_token(uow: IUnitOfWork, token_uuid: UUID):
        async with uow:
            return await uow.blacklist_token_repository.add_one(uuid=token_uuid)

    @staticmethod
    async def check_token(uow: IUnitOfWork, token_uuid: UUID) -> bool:
        async with uow:
            token = await uow.blacklist_token_repository.get_one_or_none(uuid=token_uuid)
            return token is not None

    @staticmethod
    async def get_all_tokens(uow: IUnitOfWork):
        async with uow:
            return await uow.blacklist_token_repository.get_all()
