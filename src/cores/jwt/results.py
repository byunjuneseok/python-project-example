from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str = "bearer"
    token: str
    expires_in: int


class EncodeResult(BaseModel):
    access_token: Token
    refresh_token: Token


class DecodeResult(BaseModel):
    iss: str
    sub: str
    iat: datetime
    exp: datetime
    scope: str

    def is_include_scope(self, scope: str) -> bool:
        return scope in set(self.scope.split(","))

    @property
    def role(self) -> str:
        return self.sub.split(":")[0]

    @property
    def identifier(self) -> int:
        return int(self.sub.split(":")[1])
