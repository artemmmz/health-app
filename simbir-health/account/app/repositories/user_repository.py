from abc import ABC, abstractmethod

from sqlmodel import select

from app.models.user_models import User, AccountCreation
from app.repositories.base import SQLModelRepository, AbstractRepository
from app.utils.enums import Role


class IUserRepository(AbstractRepository, ABC):
    @abstractmethod
    async def get_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_doctor(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all_doctors(self):
        raise NotImplementedError

    @abstractmethod
    async def set_role(self, user_id: int, role: Role):
        raise NotImplementedError


class UserRepository(SQLModelRepository, IUserRepository):
    model = User

    async def add_user(
            self, data: AccountCreation):

    async def get_user(self, user_id: int) -> User:
        return await self.get_one(id=user_id)

    async def get_doctor(self, user_id: int) -> User:
        statement = (
            select(self.model)
                     .filter_by(id=user_id)
                     .where(self.model.c.roles.contains([Role.DOCTOR.value]))
         )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_doctors(self):
        statement = (
            select(self.model)
                    .where(self.model.c.roles.contains([Role.DOCTOR.value]))
        )
        raw_result = await self.session.execute(statement)
        return [result.scalar_one() for result in raw_result.all()]

    async def add_role(self, user_id: int, role: Role):
        ...

    async def remove_role(self, user_id: int, relation_id: int):
        ...

