from abc import ABC, abstractmethod
from typing import List

from sqlmodel import select

from app.models.user_models import User
from app.repositories.base import SQLModelRepository, AbstractDBRepository


class IUserRepository(AbstractDBRepository, ABC):
    """Interface for user repository."""
    @abstractmethod
    async def add_user(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, only_active: bool = True, **data):
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(
        self,
        only_active: bool = True,
        offset: int = None,
        limit: int = None,
        **data,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_users_by_ids(
        self,
        user_ids: List[int],
        only_active: bool = True,
        offset: int = None,
        limit: int = None,
        full_name: str = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: int, **data):
        raise NotImplementedError

    @abstractmethod
    async def deactivate_user(self, user_id: int):
        raise NotImplementedError


class UserRepository(IUserRepository, SQLModelRepository, ABC):
    """User repository for working with data via sqlmodel and sqlalchemy."""
    model = User

    async def add_user(self, data: dict) -> User:
        instance = self.model(**data)
        return await self.add_one(instance)

    async def get_user(self, only_active: bool = True, **data) -> User:
        if only_active:
            data['is_active_'] = True
        return await self.get_one(**data)

    async def get_all_users(
        self,
        only_active: bool = True,
        offset: int = None,
        limit: int = None,
        **data,
    ) -> list[User]:
        if only_active:
            data['is_active_'] = True
        return await self.get_all(offset, limit, **data)

    async def get_users_by_ids(
        self,
        user_ids: List[int],
        only_active: bool = True,
        offset: int = None,
        limit: int = None,
        full_name: str = None,
    ) -> list[User]:
        statement = select(self.model).where(self.model.id_.in_(user_ids))  # type: ignore
        if full_name:
            statement = statement.where(
                (self.model.first_name + ' ' + self.model.last_name).like(  # type: ignore
                    full_name
                )
            )
        if only_active:
            statement = statement.filter_by(is_active_=True)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        return await self._fetch_all(statement)

    async def deactivate_user(self, user_id: int) -> User:
        return await self.update_user(user_id=user_id, is_active_=False)

    async def update_user(self, user_id: int, **data) -> User:
        return await self.update_one(filter_data={'id_': user_id}, **data)
