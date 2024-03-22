from applications.base.schemas.base_schema import BaseSchema


class ErrorResponse(BaseSchema):
    code: str
    message: str
    extra: dict | None = None
