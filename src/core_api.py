from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware

from applications.base.exceptions.handlers import (
    bad_request_handler,
    forbidden_handler,
    not_found_handler,
    request_validation_error_handler,
    too_many_requests_handler,
    unauthorized_handler,
)
from applications.base.middlewares.async_session_middleware import (
    AsyncSessionMiddleware,
)
from applications.base.middlewares.cors import create_cors_middleware
from applications.core_api.core.main import router as main_router
from applications.core_api.settings import Settings
from containers.main import MainContainer
from contexts.rate_limit.exceptions import TooManyRequestsException
from cores.exceptions.exceptions.bad_request_exception import BadRequestException
from cores.exceptions.exceptions.forbidden_exception import ForbiddenException
from cores.exceptions.exceptions.not_found_exception import NotFoundException
from cores.exceptions.unauthorized_exception import UnauthorizedException


def initialize_middlewares(stage: str) -> list:
    return [
        Middleware(AsyncSessionMiddleware),
        create_cors_middleware(stage=stage),
    ]


def create_app():
    container = MainContainer()
    settings = Settings()
    app = FastAPI(
        title="example",
        middleware=initialize_middlewares(stage=settings.stage),
        openapi_url=None if settings.stage == "prod" else "/core/docs/openapi.json",
        docs_url=None if settings.stage == "prod" else "/core/docs",
        redoc_url=None,
    )
    app.container = container
    app.include_router(main_router, prefix="/core")

    app.add_exception_handler(BadRequestException, bad_request_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_handler)
    app.add_exception_handler(ForbiddenException, forbidden_handler)
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(TooManyRequestsException, too_many_requests_handler)

    # startup events
    app.add_event_handler(
        "startup", container.infra().redis_async_pool_manager().init_redis_pool
    )

    # shutdown events
    app.add_event_handler(
        "shutdown", container.infra().redis_async_pool_manager().close_redis_pool
    )

    @app.get("/system/liveness")
    def live():
        return {"message": "ok"}

    return app
