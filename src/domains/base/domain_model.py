from typing import Self, TypeVar

from pydantic import BaseModel, ConfigDict

from infra.rdb.base.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity: T) -> Self:
        return cls.model_validate(entity)
