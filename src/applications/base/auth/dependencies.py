from dependency_injector.wiring import inject, Provide
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials

from applications.base.auth.auth import Auth
from applications.base.auth.bearer import HTTPAPIBearer
from cores.exceptions.unauthorized_exception import UnauthorizedException
from cores.jwt.client import JWT
from cores.jwt.enums import AuthenticationCodeEnum
from cores.jwt.exceptions import JwtDecodeException


@inject
async def auth_api(
    request: Request,
    roles: set[str],
    token: HTTPAuthorizationCredentials,
    scope_to_verify: str,
    jwt: JWT = Depends(Provide["core.jwt"]),
) -> Auth:
    try:
        result = jwt.decode(token.credentials, scope_to_verify=scope_to_verify)
    except JwtDecodeException as e:
        raise UnauthorizedException(code=e.code, message=e.message)
    if roles and result.role not in roles:
        raise UnauthorizedException(
            code=AuthenticationCodeEnum.INVALID_TOKEN, message="사용자 토큰이 아닙니다."
        )
    # set_user({"id": result.identifier})  # sentry
    return Auth(user_id=result.identifier, role=result.role, token_payload=result)


async def auth_user_api(
    request: Request, token: HTTPAuthorizationCredentials = Depends(HTTPAPIBearer())
):
    return await auth_api(
        request, roles={"user"}, token=token, scope_to_verify="core-api:v1:user"
    )


async def auth_owner_api(
    request: Request, token: HTTPAuthorizationCredentials = Depends(HTTPAPIBearer())
):
    return await auth_api(
        request, roles={"owner"}, token=token, scope_to_verify="core-api:v1:owner"
    )
