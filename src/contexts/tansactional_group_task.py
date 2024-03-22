from asyncio import TaskGroup
from typing import Self

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession


class TransactionalTaskGroup(TaskGroup):
    commit: bool
    sessions = set()

    def __init__(self, commit=False, **kwargs):
        self.commit = commit
        super().__init__(**kwargs)

    @inject
    def _get_session(
        self, session: async_scoped_session = Provide["db.provided.session"]
    ):
        return session

    def _get_session_by_task(self) -> AsyncSession | None:
        proxy = self._get_session()
        scopefunc = proxy.registry.scopefunc
        return proxy.registry.registry.get(scopefunc())

    async def __aenter__(self) -> Self:
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        try:
            ret = await super().__aexit__(exc_type, exc, tb)
        except BaseExceptionGroup as e:
            await self.rollback_sessions()
            raise e
        else:
            if self.commit:
                await self.commit_sessions()
            return ret
        finally:
            await self.remove_sessions()

    async def rollback_sessions(self):
        for session in self.sessions:
            await session.rollback()

    async def commit_sessions(self):
        for session in self.sessions:
            await session.commit()

    async def remove_sessions(self):
        for session in self.sessions:
            await session.remove()

    def create_task(self, coro, *, name=None, context=None):
        async def wrap():
            try:
                ret = await coro
            except Exception as e:
                raise e
            else:
                return ret
            finally:
                if _task_local_session := self._get_session_by_task():
                    self.sessions.add(_task_local_session)

        return super().create_task(wrap(), name=name, context=context)
