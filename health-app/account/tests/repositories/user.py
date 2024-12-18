from unittest.mock import patch, AsyncMock

import pytest

from app.core.security import get_hashed_password
from app.exceptions import AlreadyExistsError
from app.repositories import UserRepository
from app.repositories.sqlalchemy.user_repository import IUserRepository
from tests.app import settings, event_loop  # noqa: F401
from tests.database import (
    engine,
    init_db,
    session_factory,
    session,
)  # noqa: F401
from tests.models import *  # noqa: F401


@pytest.fixture(scope='function')
async def setup_users(session, user_model_fixtures):
    session.add_all(user_model_fixtures)
    await session.commit()


@pytest.fixture(scope='function', autouse=True)
async def user_repository(session, setup_users) -> UserRepository:
    return UserRepository(session)


@pytest.fixture(scope='function')
async def mock_user_repository():
    with patch(
        'app.repositories.sqlalchemy.UserRepository', new_callable=AsyncMock
    ) as mock_user_repository:
        mock_repository_instance = mock_user_repository.return_value
        yield mock_repository_instance


@pytest.mark.asyncio
class TestUserRepository:
    """Tests for user repository."""

    @staticmethod
    async def test_user_create_correct(
        user_repository: IUserRepository, user_add_fixtures
    ) -> None:
        """Test that a user can be created."""

        user_fixture = user_add_fixtures[0].copy()
        user_fixture.pop('password2')
        hashed_password = get_hashed_password(user_fixture.pop('password1'))
        user_fixture['password'] = hashed_password

        instance = await user_repository.add_user(user_fixture)

        assert instance is not None
        assert instance.id_ is not None
        assert instance.username == user_add_fixtures[0]['username']
        assert instance.first_name == user_add_fixtures[0]['first_name']
        assert instance.last_name == user_add_fixtures[0]['last_name']

    @staticmethod
    async def test_user_create_incorrect_exists_username(
        user_repository: IUserRepository, user_add_fixtures, user_fixtures
    ) -> None:
        user_fixture = user_fixtures[0].copy()
        hashed_password = get_hashed_password(user_fixture.pop('password'))
        user_fixture['password'] = hashed_password

        with pytest.raises(AlreadyExistsError):
            await user_repository.add_user(user_fixture)

    @staticmethod
    async def test_get_user_correct(
        user_repository: IUserRepository, user_fixtures
    ) -> None:
        """Test that a user can be retrieved."""

        instance = await user_repository.get_user(
            username=user_fixtures[0]['username']
        )

        assert instance is not None
        assert instance.id_ == user_fixtures[0]['id_']
        assert instance.username == user_fixtures[0]['username']
        assert instance.first_name == user_fixtures[0]['first_name']
        assert instance.last_name == user_fixtures[0]['last_name']

    @staticmethod
    async def test_all_users_correct(
        user_repository: IUserRepository, user_fixtures
    ) -> None:
        """Test that all users can be retrieved."""

        instance = await user_repository.get_all_users()

        assert len(instance) > 0

    @staticmethod
    async def test_get_users_by_ids_correct(
        user_repository: IUserRepository, user_fixtures
    ) -> None:
        """Test that all users can be retrieved."""

        ids = [1, 2, 3]
        users = await user_repository.get_users_by_ids(ids)

        assert len(users) == len(ids)

    @staticmethod
    async def test_update_user_correct(
        user_repository: IUserRepository, user_fixtures
    ):
        """Test that a user can be updated."""

        user_fixture = user_fixtures[0].copy()
        new_first_name = 'Boba'
        user = await user_repository.update_user(
            user_id=user_fixture['id_'], first_name=new_first_name
        )

        assert user is not None
        assert user.id_ == user_fixture['id_']
        assert user.first_name == new_first_name
        assert user.last_name == user_fixture['last_name']

    @staticmethod
    async def test_deactivate_user_correct(
        user_repository: IUserRepository, user_fixtures
    ) -> None:
        """Test that a user can be deactivated."""

        user_fixture = user_fixtures[0]
        user = await user_repository.deactivate_user(
            user_id=user_fixture['id_']
        )

        assert user is not None
        assert user.id_ == user_fixture['id_']
        assert user.is_active is False
