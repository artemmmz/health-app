from typing import Optional

from app.uow.database import IDatabaseUnitOfWork
from app.utils.enums import Role


class RoleService:
    """Service for working with roles."""

    @staticmethod
    async def get_roles(
        uow: IDatabaseUnitOfWork, user_id: int, only_active: bool = True
    ):
        async with uow:
            return await uow.role_repository.get_roles(user_id, only_active)

    @staticmethod
    async def get_role(uow: IDatabaseUnitOfWork, user_id: int, role: Role):
        async with uow:
            return await uow.role_repository.get_one(
                user_id=user_id, role=role
            )

    @staticmethod
    async def get_all_roles(
        uow: IDatabaseUnitOfWork,
        roles: list[Role],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        async with uow:
            return await uow.role_repository.get_all_roles(
                roles=roles, offset=offset, limit=limit
            )

    @staticmethod
    async def update_roles(
        uow: IDatabaseUnitOfWork, user_id: int, roles: list[Role]
    ):
        async with uow:
            await uow.role_repository.remove_all_roles(user_id)
            result = []
            for role in roles:
                result_role = await uow.role_repository.add_or_activate_role(
                    user_id, role
                )
                result.append(result_role)
            return result

    @staticmethod
    async def add_role(uow: IDatabaseUnitOfWork, user_id: int, role: Role):
        async with uow:
            return await uow.role_repository.add_role(user_id, role)

    @staticmethod
    async def remove_role(uow: IDatabaseUnitOfWork, user_id: int, role: Role):
        async with uow:
            return await uow.role_repository.remove_role(user_id, role)
