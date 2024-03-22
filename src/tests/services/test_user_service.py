from unittest.mock import Mock

import pytest

from containers.main import MainContainer
from domains.user.models.user import User
from infra.rdb.users.user_entity import UserEntity
from infra.rdb.users.user_repository import UserRepository


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user(self, test_container: MainContainer):
        # arrange
        user_repository = Mock(spec=UserRepository)
        user_repository.create.return_value = UserEntity(
            id=1,
            username="username",
            password="hashed",
            phone="1234567890",
        )

        # act
        with test_container.core.override_providers(password_handler=Mock()):
            with test_container.infra.override_providers(
                user_repository=user_repository
            ):
                user = await test_container.user_service().create_user(
                    user=User(
                        username="username",
                        password="pwd",
                        phone="1234567890",
                    )
                )

        # assert
        assert user.username == "username"
