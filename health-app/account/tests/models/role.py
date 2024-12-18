import pytest

from pydantic_core._pydantic_core import ValidationError

from app.models.role_models import UserRole
from app.utils.enums import Role


@pytest.fixture(scope='function')
def role_fixtures():
    return [
        {
            'id_': 1,
            'user_id': 1,
            'role': Role.USER,
        },
        {
            'id_': 2,
            'user_id': 1,
            'role': Role.ADMIN,
        },
        {
            'id_': 3,
            'user_id': 2,
            'role': Role.USER,
        },
        {
            'id_': 4,
            'user_id': 2,
            'role': Role.DOCTOR,
        },
        {
            'id_': 5,
            'user_id': 3,
            'role': Role.USER,
        },
        {'id_': 6, 'user_id': 3, 'role': Role.MANAGER, 'is_active_': False},
        {
            'id_': 7,
            'user_id': 3,
            'role': Role.DOCTOR,
        },
        {
            'id_': 8,
            'user_id': 4,
            'role': Role.USER,
        },
        {
            'id_': 9,
            'user_id': 5,
            'role': Role.USER,
        },
    ]


@pytest.fixture(scope='function')
def role_model_fixtures(role_fixtures):
    models = []
    for __fixture in role_fixtures:
        fixture = __fixture.copy()
        fixture.pop('id_')
        instance = UserRole(**fixture)
        models.append(instance)
    return models


@pytest.fixture(scope='function')
def role_instance():
    return UserRole(id_=1, user_id=1, role=Role.ADMIN)


class TestUserRole:
    @staticmethod
    def test_correct():
        instance = UserRole(role=Role.USER, user_id=1)
        UserRole.model_validate(instance)

        assert instance.role == Role.USER
        assert instance.user_id == 1
        assert instance.is_active is True

    @staticmethod
    def test_incorrect():
        with pytest.raises(ValidationError):
            instance = UserRole(role='User', user_id=1)
            UserRole.model_validate(instance)
