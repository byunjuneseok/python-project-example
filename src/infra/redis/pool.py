import asyncio
import socket

from redis import exceptions
from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as RedisAsync
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff


class RedisAsyncPoolManager:
    pool: ConnectionPool | None = None
    client: RedisAsync | None = None

    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db

    async def init_redis_pool(self):
        self.pool = ConnectionPool.from_url(
            # connection information
            url=f"redis://{self.host}",
            port=self.port,
            # management
            health_check_interval=10,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            socket_keepalive=True,
            # data
            encoding="utf-8",
            decode_responses=False,
        )
        self.pool.set_retry(Retry(ExponentialBackoff(), 3))
        self.pool.retry_on_error = [
            exceptions.ConnectionError,
            exceptions.TimeoutError,
            socket.timeout,
            asyncio.Timeout,
        ]
        self.client = RedisAsync.from_pool(self.pool)

    async def close_redis_pool(self):
        if self.pool:
            await self.pool.aclose()

    @property
    def async_client(self):
        return self.client
