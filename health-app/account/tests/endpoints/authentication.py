import pytest

from app.utils.enums import TokenStatus
from tests.app import client, event_loop, settings, mock_settings  # noqa: F401
from tests.models.user import user_add_fixtures, user_instance  # noqa: F401
from tests.models.role import role_instance  # noqa: F401
from tests.models.tokens import (
    access_token,
    refresh_token,  # noqa: F401
    refresh_auth_header,
)
from tests.services.role import mock_role_service
from tests.services.token import mock_token_service
from tests.services.user import mock_user_service


@pytest.mark.usefixtures(
    'mock_role_service', 'mock_token_service', 'mock_user_service'
)
class TestAuthentication:
    def test_signup_correct(self, client, user_add_fixtures):
        response = client.post(
            '/api/authentication/signup', json=user_add_fixtures[0]
        )

        assert response.status_code == 200
        assert response.json().get('access_token') is not None
        assert response.json().get('refresh_token') is not None

    @staticmethod
    def test_signin_correct(client, user_instance):
        response = client.post(
            '/api/authentication/signin',
            json={'username': 'username', 'password': '<PASSWORD>'},
        )

        assert response.status_code == 200
        assert response.json().get('access_token') is not None
        assert response.json().get('refresh_token') is not None

    @staticmethod
    def test_signout_correct(client, refresh_auth_header):
        response = client.put(
            '/api/authentication/signout',
            headers=refresh_auth_header,
        )

        assert response.status_code == 200
        assert response.json()['status'] == 'ok'

    @staticmethod
    def test_validate_correct(client, access_token):
        response = client.get(
            '/api/authentication/validate',
            params={'access_token': f'{access_token}'},
        )

        assert response.status_code == 200

        data = response.json()

        assert data['sub'] == 'username'
        assert data['user_id'] == 1
        assert data['status'] == TokenStatus.ACTIVE

    @staticmethod
    @pytest.mark.parametrize(
        'endpoint',
        ['/api/authentication/access', '/api/authentication/refresh'],
    )
    def test_access_refresh_correct(client, endpoint, refresh_auth_header):
        response = client.post(endpoint, headers=refresh_auth_header)

        assert response.status_code == 200

        data = response.json()
        assert data.get('access_token') is not None

        if 'refresh' in endpoint:
            assert data.get('refresh_token') is not None
