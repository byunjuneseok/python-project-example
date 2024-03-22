from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from cores.exceptions.unauthorized_exception import UnauthorizedException
from cores.jwt.enums import AuthenticationCodeEnum


class HTTPAPIBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise UnauthorizedException(
                    code=AuthenticationCodeEnum.INVALID_TOKEN,
                    message="토큰이 올바르게 입력되지 않았습니다.",
                )
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException(
                    code=AuthenticationCodeEnum.INVALID_TOKEN,
                    message="토큰이 올바르게 입력되지 않았습니다.",
                )
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
