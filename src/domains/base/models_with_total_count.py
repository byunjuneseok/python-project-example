from typing import Generic, TypeVar

from domains.base.domain_model import DomainModel

T = TypeVar("T", bound=DomainModel)


class ModelsWithTotalCount(Generic[T]):
    def __init__(self, total_count: int, items: list[T]):
        self.total_count = total_count
        self.items = items
