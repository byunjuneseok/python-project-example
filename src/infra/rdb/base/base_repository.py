from typing import Generic, Type, TypeVar

from sqlalchemy import func, Label, Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_scoped_session

from infra.rdb.base.base_entity import BaseEntity
from infra.rdb.base.mysql_error_exception import MySQLErrorException
from infra.rdb.base.results import ResultWithTotalCount

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    entity: Type[T]
    session: async_scoped_session

    def __init__(self, entity: Type[T], session: async_scoped_session):
        self.entity = entity
        self.session = session

    @property
    def table(self):
        return BaseEntity.metadata.tables[self.entity.__tablename__]

    async def create(self, **kwargs) -> T:
        self.session.add(entity := self.entity(**kwargs))
        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            raise MySQLErrorException(e)
        return entity

    async def find_by_id(self, id: int) -> T | None:
        stmt = select(self.entity).where(
            self.entity.id == id,
            self.entity.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    def get_total_count_expression(self) -> Label:
        return func.count(self.entity.id).over().label("total_count")

    def select_for_pagination(self) -> select:
        return select(
            self.entity,
            self.get_total_count_expression(),
        )

    @staticmethod
    def parse_paginated_result(result: Result) -> ResultWithTotalCount[T]:
        result = result.all()
        total_count = result[0].total_count if result else 0
        entities = [entity for entity, _ in result] if result else []
        return ResultWithTotalCount[T](items=entities, total_count=total_count)

    async def persist(self, entity: T) -> None:
        self.session.add(entity)
        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            raise MySQLErrorException(e)

    async def persist_all(self, entities: list[T]) -> None:
        self.session.add_all(entities)
        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            raise MySQLErrorException(e)
