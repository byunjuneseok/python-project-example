import json
from functools import partial

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from contexts.rate_limit.exceptions import TooManyRequestsException
from cores.exceptions.exceptions.base_service_exception import BaseServiceException


async def base_handler(request: Request, exc: BaseServiceException, status_code: int) -> Response:
    return JSONResponse(
        status_code=status_code,
        content={"code": exc.code, "message": exc.message},
    )


bad_request_handler = partial(base_handler, status_code=400)
unauthorized_handler = partial(base_handler, status_code=401)
forbidden_handler = partial(base_handler, status_code=403)
not_found_handler = partial(base_handler, status_code=404)


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> Response:
    errors = exc.errors()
    assertion_messages = ""

    if any([error["type"] == "assertion_error" for error in errors]):
        for error in errors:
            try:
                assertion_messages += error["msg"].split(",")[1].strip()
            except Exception:
                pass

    extra = assertion_messages if assertion_messages else errors

    try:
        json.dumps(extra)
    except Exception:
        try:
            if isinstance(extra, list):
                extra = [str(error) for error in extra]
        except Exception:
            extra = None

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "UNPROCESSABLE_ENTITY",
            "message": "요청 입력이 잘못되었습니다.",
            "extra": extra,
        },
    )


async def too_many_requests_handler(request: Request, exc: TooManyRequestsException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "code": "TOO_MANY_REQUESTS",
            "title": "요청이 너무 많습니다.",
            "message": "요청이 너무 많습니다.",
        },
    )
