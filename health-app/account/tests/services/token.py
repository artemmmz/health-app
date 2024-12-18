from unittest.mock import patch

import pytest

from app.services import TokenService
from tests.repositories.blacklist_token import (
    mock_blacklist_token_repository,
)  # noqa: F401
from tests.utils.uow import mock_inmemory_uow


@pytest.fixture(scope='function')
async def mock_token_service():
    with (
        patch.object(TokenService, 'blacklist_token', return_value=None),
        patch.object(
            TokenService, 'check_blacklist_token', return_value=False
        ),
        patch.object(TokenService, 'get_all_blocked_tokens', return_value=[]),
        patch.object(TokenService, 'revoke_token', return_value=None),
    ):
        yield


@pytest.mark.asyncio
class TestTokenService:
    @staticmethod
    async def test_blacklist_token(mock_inmemory_uow):
        token_uuid = '<token-uuid>'
        await TokenService.blacklist_token(mock_inmemory_uow, token_uuid)

        mock_inmemory_uow.blacklist_token_repository.add_token.assert_called_once()
        args = mock_inmemory_uow.blacklist_token_repository.add_token.call_args_list[
            0
        ][
            0
        ]

        assert args[0] == token_uuid

    @staticmethod
    async def test_check_blacklist_token(mock_inmemory_uow):
        token_uuid = '<token-uuid>'
        await TokenService.check_blacklist_token(mock_inmemory_uow, token_uuid)

        mock_inmemory_uow.blacklist_token_repository.exists_token.assert_called_once()
        args = mock_inmemory_uow.blacklist_token_repository.exists_token.call_args_list[
            0
        ][
            0
        ]

        assert args[0] == token_uuid

    @staticmethod
    async def test_get_all_blocked_tokens(mock_inmemory_uow):
        await TokenService.get_all_blocked_tokens(mock_inmemory_uow)

        mock_inmemory_uow.blacklist_token_repository.get_all_tokens.assert_called_once()

    @staticmethod
    async def test_revoke_token(mock_inmemory_uow):
        token_uuid = '<token-uuid>'
        await TokenService.revoke_token(mock_inmemory_uow, token_uuid)

        mock_inmemory_uow.blacklist_token_repository.remove_token.assert_called_once()
        args = mock_inmemory_uow.blacklist_token_repository.remove_token.call_args[
            0
        ][
            0
        ]

        assert args == token_uuid
