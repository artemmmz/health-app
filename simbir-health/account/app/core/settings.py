import secrets
from enum import Enum

from pydantic import AnyHttpUrl, computed_field, field_validator
from pydantic_settings import BaseSettings


class Mode(str, Enum):
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


class Settings(BaseSettings):
    # APPLICATION
    MODE: Mode = Mode.DEVELOPMENT

    # DATABASE
    POSTGRES_PROTOCOL: str = 'postgresql+asyncpg'
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_ARGUMENTS: dict[str, str | int | float]

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f'{self.POSTGRES_PROTOCOL}://'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}@'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}/'
            f'{self.POSTGRES_DB}'
        )

    # SECURITY
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENCRYPT_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl] = ['*']

    @field_validator('BACKEND_CORS_ORIGINS')
    def assemble_backend_cors_origins(cls, v: str | list[str]):
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        else:
            raise ValueError(v)


settings = Settings()
