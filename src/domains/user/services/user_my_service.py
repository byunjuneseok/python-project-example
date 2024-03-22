from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from cores.exceptions.exceptions.not_found_exception import NotFoundException
from domains.user.models.user import User
from infra.rdb.base.base_repository import BaseRepository
from infra.rdb.users.user_entity import UserEntity
from infra.rdb.users.user_repository import UserRepository


class UserMyService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_me(self, user_id: int) -> User | None:
        if user := await self.user_repository.get_by_id(user_id):
            return User(
                id=user.id,
                username=user.username,
                password=user.password,
                phone=user.phone,
            )
        else:
            raise NotFoundException(
                code="USER_DOES_NOT_EXIST", message="해당 유저가 존재하지 않습니다."
            )

    async def get_me_copy(self, user_id: int) -> User | None:
        session = self.user_repository.session
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user:
            return User(
                id=user.id,
                username=user.username,
                password=user.password,
                phone=user.phone,
            )
        else:
            raise NotFoundException(
                code="USER_DOES_NOT_EXIST", message="해당 유저가 존재하지 않습니다."
            )
