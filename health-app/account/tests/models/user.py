import re
from typing import Any

import pytest
from pydantic_core._pydantic_core import ValidationError

from app.core.security import get_hashed_password
from app.models.user_models import User, UserAdd


@pytest.fixture(scope='function')
def user_fixtures() -> list[dict[str, Any]]:
    """Test user datas"""
    return [
        {
            'id_': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'Password12/',
        },
        {
            'id_': 2,
            'first_name': 'Alex',
            'last_name': 'Fisherman',
            'username': 'dr_fisherman',
            'password': 'Password12/',
        },
        {
            'id_': 3,
            'first_name': 'Steve',
            'last_name': 'Minecraft',
            'username': 'minecraft',
            'password': 'Password12/',
        },
        {
            'id_': 4,
            'first_name': 'Po',
            'last_name': 'Smith',
            'username': 'po_smith',
            'password': 'Password12/',
            'is_active_': False,
        },
        {
            'id_': 5,
            'first_name': 'Jack',
            'last_name': 'Oltman',
            'username': 'oltman',
            'password': 'Password12/',
        },
    ]


@pytest.fixture(scope='function')
def user_model_fixtures(user_fixtures: list[dict[str, Any]]) -> list[User]:
    models = []
    for _user_fixture in user_fixtures:
        user_fixture = _user_fixture.copy()
        user_fixture.pop('id_')
        password = user_fixture.pop('password')
        hashed_password = get_hashed_password(password)
        instance = User(**user_fixture, password=hashed_password)
        models.append(instance)
    return models


@pytest.fixture(scope='function')
def user_add_fixtures() -> list[dict[str, Any]]:
    return [
        {
            'first_name': 'Albert',
            'last_name': 'Smith',
            'username': 'albertsmith',
            'password1': 'Password12/',
            'password2': 'Password12/',
        }
    ]


@pytest.fixture(scope='function')
def user_instance():
    return User(
        id_=1,
        first_name='first',
        last_name='last',
        username='user',
        password=get_hashed_password('<PASSWORD>'),
    )


class TestUser:
    @staticmethod
    def test_user_correct(user_fixtures: list[dict]):
        test_data: dict = user_fixtures[0].copy()
        instance = User(**test_data)
        User.model_validate(instance)

        assert instance.first_name == user_fixtures[0]['first_name']
        assert instance.last_name == user_fixtures[0]['last_name']
        assert instance.username == user_fixtures[0]['username']
        assert instance.password == user_fixtures[0]['password']

    @staticmethod
    def test_user_incorrect_username_1(user_fixtures):
        test_data = user_fixtures[0].copy()
        test_data['username'] = 'JohnDoe'
        with pytest.raises(ValidationError):
            User.model_validate_strings(test_data)

    @staticmethod
    def test_user_incorrect_username_2(user_fixtures):
        test_data = user_fixtures[0].copy()
        test_data['username'] = 'john doe'
        with pytest.raises(ValidationError):
            User.model_validate_strings(test_data)

    @staticmethod
    def test_user_incorrect_username_3(user_fixtures):
        test_data = user_fixtures[0].copy()
        test_data['username'] = 'john.doe'
        with pytest.raises(ValidationError):
            User.model_validate_strings(test_data)


class TestUserAdd:
    @staticmethod
    def test_user_add_correct(user_add_fixtures):
        instance = UserAdd(**user_add_fixtures[0])
        UserAdd.model_validate(instance)

        assert instance.first_name == user_add_fixtures[0]['first_name']
        assert instance.last_name == user_add_fixtures[0]['last_name']
        assert instance.username == user_add_fixtures[0]['username']
        assert (
            instance.password1.get_secret_value()
            == user_add_fixtures[0]['password1']
        )
        assert instance.password1 == instance.password2

    @staticmethod
    def test_user_add_incorrect_password_length(user_add_fixtures):
        data = user_add_fixtures[0].copy()
        data['password1'] = data['password2'] = 'Ps1/'  # 5 characters

        assert len(data['password1']) < 6
        assert re.search(r'[A-Z]', data['password1'])
        assert re.search(r'[a-z]', data['password1'])
        assert re.search(r'[0-9]', data['password1'])
        assert re.search(r'\W', data['password1'])
        with pytest.raises(ValidationError):
            User.model_validate_strings(data)

    @staticmethod
    def test_user_add_incorrect_password_uppercase(user_add_fixtures):
        data = user_add_fixtures[0].copy()
        new_password = data['password1'].lower()
        data['password1'] = data['password2'] = new_password

        assert len(data['password1']) >= 6
        assert not re.search(r'[A-Z]', data['password1'])
        assert re.search(r'[a-z]', data['password1'])
        assert re.search(r'[0-9]', data['password1'])
        assert re.search(r'\W', data['password1'])
        with pytest.raises(ValidationError):
            User.model_validate_strings(data)

    @staticmethod
    def test_user_add_incorrect_password_lowercase(user_add_fixtures):
        data = user_add_fixtures[0].copy()
        new_password = data['password1'].upper()
        data['password1'] = data['password2'] = new_password

        assert len(data['password1']) >= 6
        assert re.search(r'[A-Z]', data['password1'])
        assert not re.search(r'[a-z]', data['password1'])
        assert re.search(r'[0-9]', data['password1'])
        assert re.search(r'\W', data['password1'])
        with pytest.raises(ValidationError):
            User.model_validate_strings(data)

    @staticmethod
    def test_user_add_incorrect_password_numbers(
        user_add_fixtures: list[dict[str, Any]]
    ):
        data = user_add_fixtures[0].copy()
        new_password = 'Password/'
        data['password1'] = data['password2'] = new_password

        assert len(data['password1']) >= 6
        assert re.search(r'[A-Z]', data['password1'])
        assert re.search(r'[a-z]', data['password1'])
        assert not re.search(r'[0-9]', data['password1'])
        assert re.search(r'\W', data['password1'])
        with pytest.raises(ValidationError):
            User.model_validate_strings(data)

    @staticmethod
    def test_user_add_incorrect_password_special(
        user_add_fixtures: list[dict[str, Any]]
    ):
        data = user_add_fixtures[0].copy()
        new_password = 'Password12'
        data['password1'] = data['password2'] = new_password

        assert len(data['password1']) >= 6
        assert re.search(r'[A-Z]', data['password1'])
        assert re.search(r'[a-z]', data['password1'])
        assert re.search(r'[0-9]', data['password1'])
        assert not re.search(r'\W', data['password1'])
        with pytest.raises(ValidationError):
            User.model_validate_strings(data)

    @staticmethod
    def test_user_add_incorrect_passwords_match(
        user_add_fixtures: list[dict[str, Any]]
    ):
        data = user_add_fixtures[0].copy()
        data['password1'] = 'Password12/'
        data['password2'] = 'Password12/+'

        with pytest.raises(ValidationError):
            User.model_validate_strings(data)
