from domains.base.domain_model import DomainModel


class User(DomainModel):
    id: int | None = None
    username: str
    password: str
    phone: str
