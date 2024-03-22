from async_typer import AsyncTyper

from containers.main import MainContainer


def create_app() -> AsyncTyper:
    app = AsyncTyper()
    container = MainContainer()

    app.add_event_handler("startup", container.infra().redis_async_pool_manager().init_redis_pool)
    app.add_event_handler("shutdown", container.infra().redis_async_pool_manager().close_redis_pool)

    @app.command()
    def check_dependencies():
        container.check_dependencies()

    @app.async_command()
    async def create_all():
        await container.infra().rdb().create_all()

    @app.async_command()
    async def drop_all():
        await container.infra().rdb().drop_all()

    return app


if __name__ == "__main__":
    try:
        create_app().__call__()
    except Exception as e:
        payload = getattr(e, "__typer_developer_exception__")
        delattr(e, "__typer_developer_exception__")  # This cause missing exception in sentry. =/
        # sentry_sdk.capture_exception(e)
        setattr(e, "__typer_developer_exception__", payload)
        raise e
