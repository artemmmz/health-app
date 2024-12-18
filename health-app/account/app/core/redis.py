"""Module for manage redis connection."""

from redis.asyncio import ConnectionPool, Redis

from app.core.settings import settings

pool = ConnectionPool.from_url(settings.REDIS_URL)


def create_redis():
    """Create redis connection instance."""
    return Redis(connection_pool=pool)
