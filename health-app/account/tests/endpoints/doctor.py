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
class TestDoctor:
    @staticmethod
    def test_get_doctor(client, access_auth_header):
        response = client.get('/api/doctors/1', headers=access_auth_header)

        assert response.status_code == 200

    @staticmethod
    def test_get_all_doctors(client, access_auth_header):
        response = client.get('/api/doctors', headers=access_auth_header)

        assert response.status_code == 200
