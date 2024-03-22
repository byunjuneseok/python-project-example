from fastapi import APIRouter

from applications.core_api.core.v1.router import core_api_v1_router

router = APIRouter()
router.include_router(core_api_v1_router, prefix="/v1")
