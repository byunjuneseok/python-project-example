from cores.exceptions.exceptions.base_service_exception import BaseServiceException


class NotFoundException(BaseServiceException):
    code = "NOT_FOUND"
