import datetime
import secrets
from enum import Enum
from pathlib import Path
from urllib.parse import urlencode

from pydantic import AnyHttpUrl, computed_field, field_validator
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Mode(str, Enum):
    """Application mode enum class."""

    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


class Settings(BaseSettings):
    """Settings class."""

    # APPLICATION
    MODE: Mode = Mode.DEVELOPMENT

    # DATABASE
    POSTGRES_PROTOCOL: str = 'postgresql+asyncpg'
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_ARGUMENTS: dict[str, str | int | float] | None = None

    @computed_field  # type: ignore
    @property
    def POSTGRES_ARGUMENTS_URL(self) -> str:
        if self.POSTGRES_ARGUMENTS is None:
            return ''
        return urlencode(self.POSTGRES_ARGUMENTS)

    @computed_field  # type: ignore
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f'{self.POSTGRES_PROTOCOL}://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}?'
            f'{self.POSTGRES_ARGUMENTS_URL}'
        )

    # KAFKA
    KAFKA_PROTOCOL: str = 'kafka'
    KAFKA_HOST: str
    KAFKA_PORT: int = 9092

    @computed_field  # type: ignore
    @property
    def KAFKA_BROKER(self) -> str:
        return f'{self.KAFKA_PROTOCOL}://{self.KAFKA_HOST}:{self.KAFKA_PORT}/'

    # REDIS
    REDIS_PROTOCOL: str = 'redis'
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_DB: int = 0

    @computed_field  # type: ignore
    @property
    def REDIS_URL(self) -> str:
        return (
            f'{self.REDIS_PROTOCOL}://'
            f'{self.REDIS_USER}:'
            f'{self.REDIS_PASSWORD}@'
            f'{self.REDIS_HOST}:'
            f'{self.REDIS_PORT}/'
            f'{self.REDIS_DB}?'
        )

    # SECURITY
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 180
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = [
        '*',
    ]

    @computed_field  # type: ignore
    @property
    def ACCESS_TOKEN_EXPIRE_TIMEDELTA(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @computed_field  # type: ignore
    @property
    def REFRESH_TOKEN_EXPIRE_TIMEDELTA(self) -> datetime.timedelta:
        return datetime.timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

    @field_validator('BACKEND_CORS_ORIGINS')
    @classmethod
    def assemble_backend_cors_origins(cls, v: str | list[str]):
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        else:
            raise ValueError(v)


settings = Settings(_env_file=BASE_DIR / '.env')  # type: ignore
