from domains.base.exceptions.base_service_exception import BaseServiceException


class UnauthenticatedException(BaseServiceException):
    code: str = "UNAUTHENTICATED"
