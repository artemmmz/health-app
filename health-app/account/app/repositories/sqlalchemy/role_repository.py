from abc import ABC, abstractmethod
from typing import List

from sqlmodel import select

from app.models.user_models import UserRole
from app.repositories.base import AbstractDBRepository, SQLModelRepository
from app.utils.enums import Role


class IRoleRepository(AbstractDBRepository, ABC):
    """Interface for role repository."""
    @abstractmethod
    async def add_role(self, user_id: int, role):
        raise NotImplementedError

    @abstractmethod
    async def add_or_activate_role(self, user_id: int, role: Role):
        raise NotImplementedError

    @abstractmethod
    async def remove_role(self, user_id: int, role):
        raise NotImplementedError

    @abstractmethod
    async def remove_all_roles(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_roles(self, user_id: int, only_active: bool = True):
        raise NotImplementedError

    @abstractmethod
    async def get_all_roles(
        self, roles: list[Role] = None, offset: int = None, limit: int = None
    ) -> List:
        raise NotImplementedError


class RoleRepository(IRoleRepository, SQLModelRepository, ABC):
    """Role repository for working with data via sqlmodel and sqlalchemy"""
    model = UserRole

    async def add_role(self, user_id: int, role: Role) -> UserRole:
        return await self.add_one(user_id=user_id, role=role)

    async def add_or_activate_role(self, user_id: int, role: Role) -> UserRole:
        data = {'user_id': user_id, 'role': role}
        statement = self._get_insert_update_statement(
            data, constraint='user_id_role', set_data={'is_active': True}
        ).returning(self.model)
        return await self._fetch_one(statement)

    async def remove_role(self, user_id: int, role: Role) -> UserRole:
        return await self.update_one(
            {'user_id': user_id, 'role': role}, is_active_=False
        )

    async def remove_all_roles(self, user_id: int) -> List[UserRole]:
        return await self.update_all({'user_id': user_id}, is_active_=False)

    async def get_roles(
            self, user_id: int, only_active: bool = True
    ) -> List[UserRole]:
        statement = select(self.model).filter_by(user_id=user_id)
        if only_active:
            statement = statement.filter_by(is_active_=True)
        return await self._fetch_all(statement)

    async def get_all_roles(
            self, roles: list[Role] = None, offset: int = None, limit: int = None
    ) -> List[UserRole]:
        statement = select(self.model)
        if roles:
            statement = statement.filter_by(role__in=roles)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        return await self._fetch_all(statement)
