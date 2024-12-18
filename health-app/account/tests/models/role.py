import pytest

from pydantic_core._pydantic_core import ValidationError

from app.models.role_models import UserRole
from app.utils.enums import Role


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

