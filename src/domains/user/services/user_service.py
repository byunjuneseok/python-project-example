from cores.exceptions.exceptions.not_found_exception import NotFoundException
from cores.password.handler import PasswordHandler
from domains.user.models.user import User
from infra.rdb.users.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, password_handler: PasswordHandler):
        self.user_repository = user_repository
        self.password_handler = password_handler

    async def create_user(self, user: User):
        hashed_password = self.password_handler.hash(user.password)
        await self.user_repository.create(
            username=user.username,
            password=hashed_password,
            phone=user.phone,
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        if user := await self.user_repository.get_by_id(user_id):
            return User(
                id=user.id,
                username=user.username,
                password=user.password,
                phone=user.phone,
            )
        else:
            raise NotFoundException(code="USER_DOES_NOT_EXIST", message="해당 유저가 존재하지 않습니다.")
