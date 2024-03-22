from asyncio import current_task
from typing import Type

from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import Session

from infra.rdb.base.base import Base


class AsyncDatabase:
    engines: dict[str, AsyncEngine] = {}

    def __init__(self, writer_url: str, reader_url: str, echo: bool = False) -> None:
        self.engines = {
            "writer": create_async_engine(writer_url, pool_recycle=3600, echo=echo),
            "reader": create_async_engine(reader_url, pool_recycle=3600, echo=echo),
        }
        self._session = async_scoped_session(
            scopefunc=current_task,
            session_factory=async_sessionmaker(
                class_=AsyncSession,
                sync_session_class=self.get_routing_session(),
            ),
        )

    def get_routing_session(outer_self) -> Type[Session]:  # noqa
        class RoutingSession(Session):
            def get_bind(self, mapper=None, clause=None, **kw):
                if self._flushing or isinstance(clause, (Update, Delete, Insert)):
                    return outer_self.engines["writer"].sync_engine
                else:
                    if isinstance(clause, Select):
                        # when it includes lock
                        if "FOR UPDATE" in str(clause):
                            return outer_self.engines["writer"].sync_engine

                    return outer_self.engines["reader"].sync_engine

        return RoutingSession

    async def create_all(self) -> None:
        async with self.engines["writer"].begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self) -> None:
        async with self.engines["writer"].begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @property
    def session(self) -> async_scoped_session:
        """
        use the AsyncSession via the context-local proxy
        :return: async_scoped_session
        """
        return self._session
