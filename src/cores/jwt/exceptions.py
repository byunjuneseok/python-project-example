from cores.jwt.enums import AuthenticationCodeEnum


class JwtDecodeException(Exception):
    code = AuthenticationCodeEnum.INVALID_TOKEN
    message: str = None

    def __init__(self, message):
        self.message = message


class JwtExpiredSignatureException(JwtDecodeException):
    code = AuthenticationCodeEnum.TOKEN_EXPIRED


class JwtInvalidIssuerException(JwtDecodeException):
    pass


class JwtImmatureSignatureException(JwtDecodeException):
    code = AuthenticationCodeEnum.IMMATURE_TOKEN
