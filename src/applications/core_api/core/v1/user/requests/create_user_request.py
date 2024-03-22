from pydantic import BaseModel, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class CreateUserRequest(BaseModel):
    username: str
    password: SecretStr
    phone: PhoneNumber
