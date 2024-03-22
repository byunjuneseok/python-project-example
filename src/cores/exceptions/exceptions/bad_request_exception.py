from cores.exceptions.exceptions.base_service_exception import BaseServiceException


class BadRequestException(BaseServiceException):
    code = "BAD_REQUEST"

    def __init__(self, message: str, code: str = "BAD_REQUEST"):
        super().__init__(message=message, code=code)
