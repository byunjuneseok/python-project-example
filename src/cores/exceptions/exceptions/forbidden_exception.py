from cores.exceptions.exceptions.base_service_exception import BaseServiceException


class ForbiddenException(BaseServiceException):
    code = "FORBIDDEN"
