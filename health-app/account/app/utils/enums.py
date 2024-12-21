from enum import Enum


class Role(str, Enum):
    """Roles enum."""

    USER = 'user'
    DOCTOR = 'doctor'
    ADMIN = 'admin'
    MANAGER = 'manager'


class TokenStatus(str, Enum):
    """Token status enum."""

    ACTIVE = 'active'
    EXPIRED = 'expired'
    BLACKLISTED = 'blacklisted'


class TokenType(str, Enum):
    """Token type enum."""

    ACCESS = 'access'
    REFRESH = 'refresh'


class SessionAction(str, Enum):
    """Session action enum."""
    CREATE = 'create'
    TERMINATE = 'terminate'
