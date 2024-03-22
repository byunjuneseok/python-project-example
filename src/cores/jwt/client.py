from datetime import datetime, timedelta
from typing import List

import jwt
from pydantic import ValidationError

from cores.jwt.exceptions import (
    JwtDecodeException,
    JwtExpiredSignatureException,
    JwtImmatureSignatureException,
    JwtInvalidIssuerException,
)
from cores.jwt.results import DecodeResult, EncodeResult, Token


class JWT:
    """
    https://pyjwt.readthedocs.io/en/latest/
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        issuer: str,
        access_token_lifetime: int,
        refresh_token_lifetime: int,
    ):
        self.algorithm = algorithm
        self.issuer = issuer
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime
        self.secret_key = secret_key

    def _decode(self, token: str, scope_to_verify: str) -> DecodeResult:
        try:
            payload = jwt.decode(
                token, key=self.secret_key, algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise JwtExpiredSignatureException("유효기간이 지난 토큰입니다.")
        except jwt.InvalidIssuerError:
            raise JwtInvalidIssuerException("유효하지 않은 발급자입니다.")
        except jwt.ImmatureSignatureError:
            raise JwtImmatureSignatureException("아직 유효하지 않은 토큰입니다.")
        except jwt.InvalidTokenError:  # Superclass.
            raise JwtDecodeException("유효하지 않은 토큰입니다.")
        try:
            payload = DecodeResult.model_validate(payload)
        except ValidationError:
            raise JwtDecodeException("유효하지 않은 토큰입니다.")
        if not payload.is_include_scope(scope_to_verify):
            raise JwtDecodeException("유효하지 않은 토큰입니다.")
        return payload

    def _encode(
        self, user_id: str, role: str, scopes: List[str], lifetime: int
    ) -> Token:
        payload = {
            "sub": f"{role}:{user_id}",
            "exp": datetime.utcnow() + timedelta(seconds=lifetime),
            "iat": datetime.utcnow(),
            "iss": self.issuer,
            "scope": ",".join(scopes),
        }
        token = jwt.encode(
            payload=payload, key=self.secret_key, algorithm=self.algorithm
        )
        return Token(
            token=token,
            expires_in=int(payload["exp"].timestamp()),
            token_type="bearer",
        )

    def encode(
        self,
        user_id: str,
        role: str,
        access_token_scopes: List[str],
        refresh_token_scopes: List[str],
    ) -> EncodeResult:
        access_token = self._encode(
            user_id=user_id,
            role=role,
            scopes=access_token_scopes,
            lifetime=self.access_token_lifetime,
        )
        refresh_token = self._encode(
            user_id=user_id,
            role=role,
            scopes=refresh_token_scopes,
            lifetime=self.refresh_token_lifetime,
        )
        return EncodeResult(access_token=access_token, refresh_token=refresh_token)

    def decode(self, token: str, scope_to_verify: str) -> DecodeResult:
        return self._decode(token=token, scope_to_verify=scope_to_verify)
