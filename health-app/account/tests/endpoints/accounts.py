import pytest

from tests.app import client, event_loop, settings, mock_settings  # noqa: F401
from tests.models.user import user_add_fixtures, user_instance  # noqa: F401
from tests.models.role import role_instance  # noqa: F401
from tests.models.tokens import access_token, access_auth_header  # noqa: F401
from tests.services.role import mock_role_service
from tests.services.token import mock_token_service
from tests.services.user import mock_user_service


@pytest.mark.usefixtures(
    'mock_role_service', 'mock_token_service', 'mock_user_service'
)
class TestAccounts:
    @staticmethod
    def test_get_me_correct(client, access_auth_header):
        response = client.get('/api/accounts/me', headers=access_auth_header)

        assert response.status_code == 200

    @staticmethod
    def test_update_me_correct(client, access_auth_header):
        response = client.post(
            '/api/accounts/update',
            headers=access_auth_header,
            json={
                'first_name': 'first',
                'last_name': 'last',
                'password': '<PASSWORD>',
            },
        )

        assert response.status_code == 200

    @staticmethod
    def test_get_all_users_correct(client, access_auth_header):
        response = client.get('/api/accounts/', headers=access_auth_header)

        assert response.status_code == 200

    @staticmethod
    def test_create_user_correct(client, access_auth_header):
        response = client.post(
            '/api/accounts/',
            headers=access_auth_header,
            json={
                'first_name': 'first',
                'last_name': 'last',
                'username': 'user',
                'password': '<PASSWORD>',
                'roles': ['user', 'admin'],
            },
        )

        assert response.status_code == 200

    @staticmethod
    def test_update_user_correct(client, access_auth_header):
        response = client.put(
            '/api/accounts/1',
            headers=access_auth_header,
            json={
                'first_name': 'first',
                'last_name': 'last',
                'username': 'user',
                'password': '<PASSWORD>',
                'roles': ['user', 'admin'],
            },
        )

        assert response.status_code == 200

    @staticmethod
    def test_delete_user_correct(client, access_auth_header):
        response = client.delete('/api/accounts/1', headers=access_auth_header)

        assert response.status_code == 200
