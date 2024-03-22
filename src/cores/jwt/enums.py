from enum import StrEnum


class AuthenticationCodeEnum(StrEnum):
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    IMMATURE_TOKEN = "IMMATURE_TOKEN"
