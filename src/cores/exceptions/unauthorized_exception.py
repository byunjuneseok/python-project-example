from cores.exceptions.exceptions.base_service_exception import BaseServiceException


class UnauthorizedException(BaseServiceException):
    code: str = "UNAUTHORIZED"

    def __init__(self, message: str, code: str = "UNAUTHORIZED") -> None:
        self.message = message
        self.code = code
