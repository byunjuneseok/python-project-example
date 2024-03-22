from pydantic import BaseModel

from cores.jwt.results import DecodeResult


class Auth(BaseModel):
    user_id: int
    role: str
    token_payload: DecodeResult
