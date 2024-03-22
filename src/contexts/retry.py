import asyncio
from functools import wraps

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm.exc import StaleDataError


class RetryOnStaleDataError:
    class MaxRetriesExceeded(Exception):
        pass

    def __init__(
        self,
        max_retries=5,
        retry_interval: float | None = None,
        retry_exponential_backoff: bool = False,
        exception_for_max_retries_exceeded: Exception = None,
    ):
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.retry_exponential_backoff = retry_exponential_backoff
        self.exception_for_max_retries_exceeded = (
            exception_for_max_retries_exceeded or self.MaxRetriesExceeded
        )

    @inject
    def _get_session(
        self, session: async_scoped_session = Provide["db.provided.session"]
    ):
        return session

    def __call__(self, async_func):
        @wraps(async_func)
        async def wrapper(*args, **kwargs):
            for i in range(self.max_retries):
                try:
                    return await async_func(*args, **kwargs)
                except StaleDataError as e:
                    if i == self.max_retries - 1:
                        raise self.exception_for_max_retries_exceeded from e
                    if self.retry_interval:
                        interval = (
                            self.retry_interval * (2**i)
                            if self.retry_exponential_backoff
                            else self.retry_interval
                        )
                        await asyncio.sleep(interval)
                    await self._get_session().rollback()

        return wrapper
