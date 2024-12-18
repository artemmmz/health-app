from unittest.mock import patch

import pytest

from app.services import RoleService
from tests.models.role import role_fixtures, role_instance
from tests.repositories.user import mock_user_repository  # noqa: F401
from tests.repositories.role import mock_role_repository  # noqa: F401
from tests.utils.uow import mock_db_uow


@pytest.fixture(scope='function')
def mock_role_service(role_instance):
    with (
        patch.object(RoleService, 'get_roles', return_value=[role_instance]),
        patch.object(RoleService, 'get_role', return_value=role_instance),
        patch.object(
            RoleService, 'get_all_roles', return_value=[role_instance]
        ),
        patch.object(
            RoleService, 'update_roles', return_value=[role_instance]
        ),
        patch.object(RoleService, 'add_role', return_value=role_instance),
        patch.object(RoleService, 'remove_role', return_value=role_instance),
    ):
        yield


@pytest.mark.asyncio
class TestRoleService:
    @staticmethod
    async def test_add_role(mock_db_uow, role_fixtures):
        fixture = role_fixtures[0].copy()
        fixture.pop('id_')

        await RoleService.add_role(mock_db_uow, **fixture)

        mock_db_uow.role_repository.add_role.assert_called_once()
        args = mock_db_uow.role_repository.add_role.call_args_list[0][0]

        assert args[0] == fixture['user_id']
        assert args[1] == fixture['role']

    @staticmethod
    async def test_get_all_roles(mock_db_uow, role_fixtures):
        fixture = role_fixtures[0]
        await RoleService.get_roles(mock_db_uow, fixture['user_id'])

        mock_db_uow.role_repository.get_roles.assert_called_once()
        args = mock_db_uow.role_repository.get_roles.call_args_list[0][0]

        assert args[0] == fixture['user_id']

    @staticmethod
    async def test_get_role(mock_db_uow, role_fixtures):
        fixture = role_fixtures[0]
        await RoleService.get_role(
            mock_db_uow, fixture['user_id'], fixture['role']
        )

        mock_db_uow.role_repository.get_one.assert_called_once()
        kwargs = mock_db_uow.role_repository.get_one.call_args_list[0][1]

        assert kwargs['user_id'] == fixture['user_id']
        assert kwargs['role'] == fixture['role']

    @staticmethod
    async def test_remove_role(mock_db_uow, role_fixtures):
        fixture = role_fixtures[0]

        await RoleService.remove_role(
            mock_db_uow, fixture['user_id'], fixture['role']
        )

        mock_db_uow.role_repository.remove_role.assert_called_once()
        args = mock_db_uow.role_repository.remove_role.call_args_list[0][0]

        assert args[0] == fixture['user_id']
        assert args[1] == fixture['role']
