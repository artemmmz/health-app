from abc import ABC, abstractmethod
from typing import Type, List, Any, Optional

from asyncpg import UniqueViolationError  # type: ignore
from sqlalchemy import Result
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update

from app.exceptions import NoResultError, AlreadyExistsError, AppError
from app.models.base import BaseTableModel
from app.repositories.base import AbstractRepository

_T = Type[BaseTableModel] | BaseTableModel


class IDatabaseRepository(AbstractRepository, ABC):
    @abstractmethod
    async def get_one_or_none(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, *args, **kwargs):
        raise NotImplementedError


class SQLModelRepository(IDatabaseRepository, ABC):
    """Repository for working with data via sqlmodel and sqlalchemy."""

    model: _T

    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_insert_statement(self, **data):
        statement = insert(self.model).values(**data)
        return statement

    def _get_select_statement(self, **data):
        statement = select(self.model).filter_by(**data)
        return statement

    def _get_update_statement(self, filter_data: dict, **data):
        statement = (
            update(self.model)  # type: ignore
            .filter_by(**filter_data)
            .values(**data)
            .returning(self.model)  # type: ignore
        )
        return statement

    def _get_insert_update_statement(
        self,
        data: dict,
        constraint: str | None = None,
        index_elements: list | None = None,
        set_data: dict | None = None,
    ):
        statement = self._get_insert_statement(**data).on_conflict_do_update(
            constraint=constraint, index_elements=index_elements, set_=set_data
        )
        return statement

    async def _add(self, instance: object) -> None:
        try:
            self.session.add(instance)
        except SQLAlchemyError:
            raise AppError

    async def _add_many(self, instances: list[object]) -> None:
        for instance in instances:
            await self._add(instance)

    async def _execute(self, statement) -> Result:
        try:
            return await self.session.execute(statement)
        except IntegrityError:
            raise AppError

    async def _commit(self) -> None:
        try:
            await self.session.commit()
        except IntegrityError as e:
            if (
                e.orig.sqlstate  # type: ignore
                == UniqueViolationError.sqlstate
            ):
                raise AlreadyExistsError(self.model)
            raise AppError

    async def _refresh(self, instance: object) -> None:
        await self.session.refresh(instance)

    async def _refresh_many(self, instances: list[object]) -> None:
        for instance in instances:
            await self._refresh(instance)

    async def _fetch_one(self, statement) -> _T:
        result = await self._execute(statement)
        try:
            return result.unique().scalar_one()
        except NoResultFound:
            raise NoResultError(model=self.model)

    async def _fetch_one_or_none(self, statement) -> _T | None:
        result = await self._execute(statement)
        return result.unique().scalar_one_or_none()

    async def _fetch_all(self, statement) -> List[_T]:
        raw_result = await self._execute(statement)
        return list(raw_result.scalars().all())

    async def get_one(self, **data) -> _T:
        statement = self._get_select_statement(**data)
        return await self._fetch_one(statement)

    async def get_one_or_none(self, **data) -> _T | None:
        statement = self._get_select_statement(**data)
        return await self._fetch_one_or_none(statement)

    async def get_all(
        self, offset: Optional[int] = None, limit: Optional[int] = None, **data
    ) -> list[_T]:
        statement = self._get_select_statement(**data)
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        return await self._fetch_all(statement)

    async def add_one(self, instance: Optional[_T] = None, **data) -> _T:
        if instance is None:
            instance = self.model(**data)
        await self._add(instance)
        await self._commit()
        await self._refresh(instance)
        return instance

    async def add_many(
        self, *datas: dict[str, Any], instances: Optional[List[_T]] = None
    ) -> list[_T]:
        if instances is None:
            instances = []

            for data in datas:
                instances.append(self.model(**data))

        await self._add_many(instances)
        await self._commit()
        await self._refresh_many(instances)
        return instances

    async def update_one(self, filter_data: dict, **data):
        statement = self._get_update_statement(filter_data, **data)
        return await self._fetch_one(statement)

    async def update_all(self, filter_data: dict, **data):
        statement = self._get_update_statement(filter_data, **data)
        return await self._fetch_all(statement)
