import datetime

from app.core.settings import settings


def get_now(replace_tz: bool = True) -> datetime.datetime:
    """Get not datetime in UTC."""
    dt = datetime.datetime.now(datetime.UTC)
    if replace_tz:
        dt = dt.replace(tzinfo=None)
    return dt


def get_refresh_expires() -> datetime.timedelta:
    """Get refresh `expires_in` timedelta from settings."""
    return datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


def get_access_expires() -> datetime.timedelta:
    """Get access `expires_in` timedelta from settings."""
    return datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
