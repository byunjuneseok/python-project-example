from typing import Generic, TypeVar

from infra.rdb.base.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class ResultWithTotalCount(Generic[T]):
    def __init__(self, items: list[T], total_count: int):
        self.items = items
        self.total_count = total_count
