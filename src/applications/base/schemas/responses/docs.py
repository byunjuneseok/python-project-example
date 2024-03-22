from pydantic import BaseModel

from applications.base.schemas.responses.error_response import ErrorResponse


class ErrorResponseDescription(BaseModel):
    code: str
    message: str
    description: str


def generate_docs_error_responses(
    responses: list[ErrorResponseDescription], description: str | None = None
) -> dict:
    content = """
| code | message | description |
| ---- | ------- | ----------- |
"""
    if description:
        content = description + "\n" + content
    for response in responses:
        content += (
            f"| `{response.code}` | {response.message} | {response.description} |\n"
        )
    return dict(description=content, model=ErrorResponse)
