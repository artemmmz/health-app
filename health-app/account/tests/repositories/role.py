from unittest.mock import patch, AsyncMock

import pytest

from app.exceptions import AlreadyExistsError
from app.repositories import RoleRepository
from app.utils.enums import Role
from tests.app import settings, event_loop  # noqa: F401
from tests.database import (
    engine,
    init_db,
    session_factory,
    session,
)  # noqa: F401
from tests.repositories.user import setup_users
from tests.models import *  # noqa: F401


@pytest.fixture(scope='function')
async def setup_roles(session, setup_users, role_model_fixtures):
    session.add_all(role_model_fixtures)
    await session.commit()


@pytest.fixture(scope='function')
def role_add_fixture():
    return {'user_id': 1, 'role': Role.MANAGER}


@pytest.fixture(scope='function')
def role_repository(session, setup_roles):
    return RoleRepository(session)


@pytest.fixture(scope='function')
def mock_role_repository():
    with patch(
        'app.repositories.sqlalchemy.RoleRepository', new_callable=AsyncMock
    ) as mock_repository:
        mock_repository_instance = mock_repository.return_value

        yield mock_repository_instance


@pytest.mark.asyncio
class TestRoleRepository:
    @staticmethod
    async def test_add_role_correct(role_repository, role_add_fixture):
        instance = await role_repository.add_role(**role_add_fixture)

        assert instance is not None
        assert instance.user_id == role_add_fixture['user_id']
        assert instance.role == role_add_fixture['role']
        assert instance.is_active is True

    @staticmethod
    async def test_add_role_incorrect_exists_constraint(
        role_repository, role_fixtures
    ):
        fixture = role_fixtures[0].copy()
        fixture.pop('id_')
        with pytest.raises(AlreadyExistsError):
            await role_repository.add_role(**fixture)

    @staticmethod
    async def test_add_or_activate_role_correct_add(
        role_repository, role_add_fixture
    ):
        instance = await role_repository.add_or_activate_role(
            **role_add_fixture
        )

        assert instance is not None
        assert instance.user_id == role_add_fixture['user_id']
        assert instance.role == role_add_fixture['role']
        assert instance.is_active is True

    @staticmethod
    async def test_add_or_activate_role_correct_active(
        role_repository, role_fixtures
    ):
        fixture = role_fixtures[5].copy()
        fixture.pop('id_')
        fixture.pop('is_active_')
        instance = await role_repository.add_or_activate_role(**fixture)

        assert instance is not None
        assert instance.user_id == fixture['user_id']
        assert instance.role == fixture['role']
        assert instance.is_active is True

    @staticmethod
    async def test_remove_role_correct(role_repository, role_fixtures):
        fixture = role_fixtures[6].copy()
        instance = await role_repository.remove_role(
            fixture['user_id'], fixture['role']
        )

        assert instance is not None
        assert instance.id_ == fixture['id_']
        assert instance.user_id == fixture['user_id']
        assert instance.role == fixture['role']
        assert instance.is_active is False

    @staticmethod
    async def test_remove_all_roles_correct(role_repository, role_fixtures):
        user_id = 3
        instances = await role_repository.remove_all_roles(user_id)

        assert len(instances) > 0
        for instance in instances:
            assert instance.user_id == user_id
            assert instance.is_active is False

    @staticmethod
    async def test_get_roles_correct(role_repository, role_fixtures):
        user_id = 1
        instances = await role_repository.get_roles(user_id)

        assert len(instances) > 0
        for instance in instances:
            assert instance.user_id == user_id
            assert instance.is_active is True

    @staticmethod
    async def test_get_all_roles_correct(role_repository, role_fixtures): ...
