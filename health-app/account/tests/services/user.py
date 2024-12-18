from unittest.mock import patch, AsyncMock

import pytest

from app.services import UserService
from tests.models.user import user_add_fixtures, user_fixtures, user_instance
from tests.repositories.user import mock_user_repository  # noqa: F401
from tests.repositories.role import mock_role_repository  # noqa: F401
from tests.utils.uow import mock_db_uow


@pytest.fixture(scope='function')
def mock_user_service(user_instance):
    with (
        patch.object(UserService, 'add_user', return_value=user_instance),
        patch.object(UserService, 'get_user', return_value=user_instance),
        patch.object(
            UserService, 'get_user_by_id', return_value=user_instance
        ),
        patch.object(UserService, 'update_user', return_value=user_instance),
        patch.object(UserService, 'delete_user', return_value=user_instance),
        patch.object(UserService, 'get_all_users', return_value=user_instance),
        patch.object(
            UserService, 'get_users_by_ids', return_value=user_instance
        ),
        patch.object(UserService, 'update_user', return_value=user_instance),
        patch.object(UserService, 'delete_user', return_value=user_instance),
        patch.object(
            UserService, 'get_all_users', return_value=[user_instance]
        ),
        patch.object(
            UserService, 'get_users_by_ids', return_value=[user_instance]
        ),
    ):
        yield


@pytest.mark.asyncio
class TestUserService:
    @staticmethod
    async def test_add_user(mock_db_uow, user_add_fixtures):
        fixture = user_add_fixtures[0].copy()
        fixture['password'] = fixture.pop('password1')
        fixture.pop('password2')

        await UserService.add_user(mock_db_uow, fixture)

        mock_db_uow.user_repository.add_user.assert_called_once()
        args = mock_db_uow.user_repository.add_user.call_args_list[0][0][0]

        assert args['first_name'] == fixture['first_name']
        assert args['last_name'] == fixture['last_name']
        assert args['username'] == fixture['username']

    @staticmethod
    async def test_get_user(mock_db_uow, user_fixtures):
        await UserService.get_user_by_id(mock_db_uow, 1)

        mock_db_uow.user_repository.get_user.assert_called_once()
        args = mock_db_uow.user_repository.get_user.call_args_list[0][1]

        assert args['id_'] == 1

    @staticmethod
    async def get_all_users(mock_db_uow, user_fixtures):
        await UserService.get_all_users(mock_db_uow)

        mock_db_uow.user_repository.get_all_users.assert_called_once()

    @staticmethod
    async def test_update_user(mock_db_uow, user_fixtures):
        new_first_name = user_fixtures[1]['first_name']
        await UserService.update_user(
            mock_db_uow, 1, {'first_name': new_first_name}
        )

        mock_db_uow.user_repository.update_user.assert_called_once()
        args = mock_db_uow.user_repository.update_user.call_args_list[0][0]
        kwargs = mock_db_uow.user_repository.update_user.call_args_list[0][1]

        assert args[0] == 1
        assert kwargs['first_name'] == new_first_name

    @staticmethod
    async def test_delete_user(mock_db_uow):
        await UserService.delete_user(mock_db_uow, 1)

        mock_db_uow.user_repository.deactivate_user.assert_called_once()
        args = mock_db_uow.user_repository.deactivate_user.call_args_list[0][0]

        assert args[0] == 1
