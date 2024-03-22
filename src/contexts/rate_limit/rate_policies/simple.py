from redis.asyncio import Redis

from ..exceptions import TooManyRequestsException
from .base import BaseLimitPolicy


class SimpleLimitPolicy(BaseLimitPolicy):
    def __init__(self, threshold: int, period: int):
        self.threshold = threshold
        self.period = period

    async def execute(self, key: str, redis: Redis):
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, self.period)
        if count > self.threshold:
            raise TooManyRequestsException()
