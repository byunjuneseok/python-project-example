from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from infra.rdb.base.base_repository import BaseRepository
from infra.rdb.users.user_entity import UserEntity


class UserRepository(BaseRepository[UserEntity]):
    def __init__(self, session: async_scoped_session):
        super().__init__(UserEntity, session)

    async def get_by_username(self, username: str) -> UserEntity | None:
        stmt = select(UserEntity).where(
            self.entity.username == username,
            self.entity.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        stmt = select(UserEntity).where(
            self.entity.id == user_id,
            self.entity.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
