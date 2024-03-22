from functools import wraps

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import async_scoped_session


class Transactional:
    commit: bool

    def __init__(self, commit=False):
        self.commit = commit

    @inject
    def _get_session(self, session=Provide["infra.rdb.provided.session"]):
        return session

    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            session = self._get_session()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                if self.commit:
                    await session.commit()

            return result

        return _transactional

    async def __aenter__(self) -> async_scoped_session:
        """
        :return: async_scoped_session (proxied)
        """
        self.session = self._get_session()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.session.rollback()
            raise exc_value
        else:
            if self.commit:
                await self.session.commit()
