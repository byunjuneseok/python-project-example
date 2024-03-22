from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware


def create_cors_middleware(stage: str) -> Middleware:
    match stage:
        case "dev":
            allow_origins = [
                "*",
            ]
        case "prod":
            allow_origins = [
                "*",
            ]
        case _:
            allow_origins = []

    return Middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=[
            "client-request-id",
            "authorization",
            "cache-control",
        ],
    )
