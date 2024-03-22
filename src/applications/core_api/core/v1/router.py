from fastapi import APIRouter

from applications.core_api.core.v1.user.router import v1_user_router

core_api_v1_router = APIRouter()
core_api_v1_router.include_router(
    v1_user_router,
    prefix="/users",
    tags=["users"],
)
