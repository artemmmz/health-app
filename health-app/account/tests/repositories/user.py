from unittest import TestCase

from app.models.user_models import UserAdd
from app.repositories import UserRepository
from app.repositories.user_repository import IUserRepository
from tests.repositories.base import SQLModelRepositoryTestCase


class UserRepositoryTestCase(SQLModelRepositoryTestCase):
    repository: UserRepository

    def setUp(self):
        self.repository_class = UserRepository
        super().setUp()

    def __get_correct_user_add(self):
        first_name = 'John'
        last_name = 'Doe'
        username = 'johndoe'
        password1 = password2 = 'Password12/'

        test_user = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password1': password1,
            'password2': password2,
        }
        return test_user

    async def test_correct_add_user(self):
        test_user_data = self.__get_correct_user_add()
        test_user_add = UserAdd(**test_user_data)
        result = await self.repository.add_user(test_user_add)

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.first_name, test_user_add.first_name)
        self.assertEqual(result.last_name, test_user_add.last_name)
        self.assertEqual(result.username, test_user_add.username)
        self.assertNotEqual(result.password, test_user_add.password1)

    async def test_incorrect_add_user_passwords_match(self):
        test_user_data = self.__get_correct_user_add()
        test_user_data['password1'] = 'Password12/'
        test_user_data['password2'] = 'Password12/!'
        test_user_add = UserAdd(**test_user_data)
        result = await self.repository.add_user(test_user_add)
        self.assert
