import pytest

from app.core.security import create_access_token, create_refresh_token


@pytest.fixture(scope='function')
def access_token():
    return create_access_token(1, 'username')


@pytest.fixture(scope='function')
def refresh_token():
    return create_refresh_token(1, 'username')


@pytest.fixture(scope='function')
def access_auth_header(access_token):
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture(scope='function')
def refresh_auth_header(refresh_token):
    return {'Authorization': f'Bearer {refresh_token}'}
