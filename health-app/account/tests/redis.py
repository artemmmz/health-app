from unittest.mock import patch

import pytest

from redis.asyncio import ConnectionPool, Redis

from tests.app import settings


@pytest.fixture(scope='function')
async def mock_redis_connection() -> Redis:
    with patch('redis.asyncio.Redis') as MockRedis:
        mock_redis_instance: Redis = MockRedis.return_value
        yield mock_redis_instance


@pytest.fixture(scope='session')
def redis_pool(settings) -> ConnectionPool:
    return ConnectionPool.from_url(settings.REDIS_URL)


@pytest.fixture(scope='function')
async def redis(redis_pool) -> Redis:
    redis = Redis(connection_pool=redis_pool)
    yield redis
    await redis.flushdb(True)
    await redis.aclose(False)
