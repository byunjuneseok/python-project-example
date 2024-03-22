import abc

from redis.asyncio import Redis


class BaseLimitPolicy(abc.ABC):
    @abc.abstractmethod
    async def execute(self, key: str, redis: Redis): ...
