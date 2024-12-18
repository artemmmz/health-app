import logging
import uuid
from unittest.mock import patch, AsyncMock

import pytest

from app.repositories import BlacklistTokenRepository
from tests.redis import redis, redis_pool  # noqa: F401
from tests.app import settings, event_loop  # noqa: F401


@pytest.fixture(scope='module')
def blacklist_tokens():
    return [uuid.uuid4() for _ in range(10)]


@pytest.fixture(scope='function')
async def init_blacklist_tokens(redis, blacklist_tokens):
    prefix = BlacklistTokenRepository.prefix
    for token in blacklist_tokens:
        await redis.set(f'{prefix}:{token}', 'blacklisted', ex=3600)


@pytest.fixture(scope='function')
def blacklist_tokens_repository(
    redis, init_blacklist_tokens
) -> BlacklistTokenRepository:
    return BlacklistTokenRepository(redis)


@pytest.fixture(scope='function')
def mock_blacklist_token_repository():
    with patch(
        'app.repositories.redis.BlacklistTokenRepository',
        new_callable=AsyncMock,
    ) as mock_repository_class:
        mock_repository_instance = mock_repository_class.return_value

        yield mock_repository_instance


@pytest.mark.asyncio
class TestBlacklistTokenRepository:
    @staticmethod
    async def test_exist_token(
        blacklist_tokens_repository: BlacklistTokenRepository,
        redis,
        blacklist_tokens,
    ):
        result = await blacklist_tokens_repository.exists_token(
            blacklist_tokens[0]
        )
        assert result is True

    @staticmethod
    async def test_exist_token_not_exist(
        blacklist_tokens_repository: BlacklistTokenRepository,
    ):
        result = await blacklist_tokens_repository.exists_token(uuid.uuid4())

        assert result is False

    @staticmethod
    async def test_add_token(
        blacklist_tokens_repository: BlacklistTokenRepository,
    ):
        token = uuid.uuid4()
        await blacklist_tokens_repository.add_token(token)

        result = await blacklist_tokens_repository.exists_token(token)

        assert result is True

    @staticmethod
    async def test_remove_token(
        blacklist_tokens_repository: BlacklistTokenRepository, blacklist_tokens
    ):
        await blacklist_tokens_repository.remove_token(blacklist_tokens[0])

        result = await blacklist_tokens_repository.exists_token(
            blacklist_tokens[0]
        )
        assert result is False

    @staticmethod
    async def test_get_all_tokens(
        blacklist_tokens_repository: BlacklistTokenRepository,
    ):
        result = await blacklist_tokens_repository.get_all_tokens()
        print(result)
