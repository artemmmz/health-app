from unittest.mock import patch

import pytest

from tests.repositories.blacklist_token import mock_blacklist_token_repository
from tests.repositories.role import mock_role_repository
from tests.repositories.user import mock_user_repository


@pytest.fixture(scope='function')
def mock_db_uow(mock_user_repository, mock_role_repository):
    with patch('app.uow.database.SQLAlchemyUOW') as mock_uow_class:
        mock_uow_instance = mock_uow_class.return_value

        mock_uow_instance.role_repository = mock_role_repository
        mock_uow_instance.user_repository = mock_user_repository

        mock_uow_instance.__aenter__.return_value = mock_uow_instance
        mock_uow_instance.__aexit__.return_value = None
        yield mock_uow_instance


@pytest.fixture(scope='function')
def mock_inmemory_uow(mock_blacklist_token_repository):
    with patch('app.uow.inmemory.RedisUOW') as mock_uow_class:
        mock_uow_instance = mock_uow_class.return_value

        mock_uow_instance.blacklist_token_repository = (
            mock_blacklist_token_repository
        )

        mock_uow_instance.__aenter__.return_value = mock_uow_instance
        mock_uow_instance.__aexit__.return_value = None
        yield mock_uow_instance
