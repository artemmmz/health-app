from app.core.security import get_hashed_password
from app.exceptions import AppError
from app.uow.database import IDatabaseUnitOfWork


class UserService:
    """Service for working with users."""

    @staticmethod
    async def add_user(uow: IDatabaseUnitOfWork, data: dict):
        password = data['password']
        hashed_password = get_hashed_password(password)
        data['password'] = hashed_password
        async with uow:
            user = await uow.user_repository.add_user(data)
            return user

    @staticmethod
    async def get_user(
        uow: IDatabaseUnitOfWork, only_active: bool = True, **data
    ):
        async with uow:
            return await uow.user_repository.get_user(only_active, **data)

    @staticmethod
    async def get_user_by_id(
        uow: IDatabaseUnitOfWork, user_id: int, only_active: bool = True
    ):
        async with uow:
            return await uow.user_repository.get_user(only_active, id_=user_id)

    @staticmethod
    async def get_all_users(
        uow: IDatabaseUnitOfWork,
        offset: int = None,
        limit: int = None,
        only_active: bool = True,
        **data,
    ):
        async with uow:
            return await uow.user_repository.get_all_users(
                only_active, offset, limit, **data
            )

    @staticmethod
    async def get_users_by_ids(
        uow: IDatabaseUnitOfWork,
        user_ids: list[int],
        only_active: bool = True,
        offset: int = None,
        limit: int = None,
        full_name: str = None,
    ):
        async with uow:
            return await uow.user_repository.get_users_by_ids(
                user_ids, only_active, offset, limit, full_name
            )

    @staticmethod
    async def update_user(uow: IDatabaseUnitOfWork, user_id: int, data: dict):
        if data.get('password'):
            password = data['password']
            hashed_password = get_hashed_password(password)
            data['password'] = hashed_password
        if len(data) == 0:
            raise AppError
        async with uow:
            return await uow.user_repository.update_user(user_id, **data)

    @staticmethod
    async def delete_user(uow: IDatabaseUnitOfWork, user_id: int):
        async with uow:
            return await uow.user_repository.deactivate_user(user_id)
