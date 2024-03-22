from enum import StrEnum

import jwt
from dependency_injector.wiring import inject, Provide
from redis.asyncio import Redis
from starlette.requests import Request

from contexts.rate_limit.exceptions import TooManyRequestsException
from contexts.rate_limit.rate_policies.base import BaseLimitPolicy
from contexts.rate_limit.rate_policies.simple import SimpleLimitPolicy


class RateLimit:
    SimpleLimitPolicy = SimpleLimitPolicy

    class KeyBuildPolicy(StrEnum):
        NO_KEY = "no_key"
        BY_IP = "by_ip"
        BY_JWT_SUB = "by_jwt_sub"

    def __init__(
        self,
        api_name: str,
        limit_policy: BaseLimitPolicy,
        key_build_policy: KeyBuildPolicy = KeyBuildPolicy.NO_KEY,
    ):
        self.api_name = api_name
        self.limit_policy = limit_policy
        self.key_build_policy: RateLimit.KeyBuildPolicy = key_build_policy

    @inject
    def _redis(self, redis: Redis = Provide["infra.redis_async"]) -> Redis:
        return redis

    def build_key(self, request: Request) -> str:
        match self.key_build_policy:
            case RateLimit.KeyBuildPolicy.NO_KEY:
                return f"rate_limit::{RateLimit.KeyBuildPolicy.NO_KEY.value}:{self.api_name}"
            case RateLimit.KeyBuildPolicy.BY_IP:
                ip = request.client.host
                return f"rate_limit::{RateLimit.KeyBuildPolicy.BY_IP.value}:{self.api_name}:{ip}"
            case RateLimit.KeyBuildPolicy.BY_JWT_SUB:
                headers = request.headers
                if not (token := headers.get("Authorization")):
                    sub = None
                elif not token.lower().startswith("bearer "):
                    sub = None
                else:
                    try:
                        payload = jwt.decode(
                            token[7:],  # remove "Bearer "
                            algorithms=["HS512"],
                            options={"verify_signature": False},
                        )
                    except jwt.DecodeError:
                        sub = None
                    else:
                        sub = payload.get("sub")
                return f"rate_limit::{RateLimit.KeyBuildPolicy.BY_JWT_SUB.value}:{self.api_name}:{sub}"

    async def simple(self, request: Request, limit: int, period: int):
        key = self.build_key(request=request)
        count = await self._redis().incr(key)
        if count == 1:
            await self._redis().expire(key, period)
        if count > limit:
            raise TooManyRequestsException

    async def __call__(
        self,
        request: Request,
    ):
        key = self.build_key(request=request)
        await self.limit_policy.execute(key=key, redis=self._redis())
