from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from applications.base.auth.auth import Auth
from applications.base.auth.dependencies import auth_user_api
from applications.core_api.core.v1.user.requests.create_user_request import CreateUserRequest
from domains.user.models.user import User
from domains.user.services.user_service import UserService

v1_user_router = APIRouter()


@v1_user_router.post("")
@inject
async def create_user(
    body: CreateUserRequest,
    user_service: UserService = Depends(Provide["user_service"]),
):
    await user_service.create_user(
        user=User(
            username=body.username,
            password=body.password,
            phone=body.phone,
        )
    )


@v1_user_router.get("")
@inject
async def get_me(
    auth: Auth = Depends(auth_user_api),
    user_service: UserService = Depends(Provide["user_service"]),
):
    return await user_service.get_user_by_id(auth.user_id)
