import boto3
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Configuration, Factory, Provider, Resource, Singleton
from redis.asyncio import Redis

from infra.rdb.engine import AsyncDatabase
from infra.rdb.users.user_repository import UserRepository
from infra.redis.pool import RedisAsyncPoolManager


class InfraContainer(DeclarativeContainer):
    config = Configuration()

    # Relational Database Layer.
    rdb = Singleton(
        AsyncDatabase,
        writer_url=config.rdb.writer_url,
        reader_url=config.rdb.reader_url,
        echo=config.echo,
    )
    user_repository = Factory(UserRepository, session=rdb.provided.session)

    # Cache layer.
    redis_async_pool_manager: Provider[RedisAsyncPoolManager] = Singleton(
        RedisAsyncPoolManager,
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
    )
    redis_async: Provider[Redis] = Callable(redis_async_pool_manager.provided.async_client)

    # AWS Layer.
    boto3_session = Resource(boto3.session.Session)
