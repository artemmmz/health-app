from abc import ABC

from app.models.token_models import BlacklistToken
from app.repositories.sqlalchemy.base import AbstractDBRepository, SQLModelRepository


class IBlacklistRepository(AbstractDBRepository, ABC):
    """Interface for blacklist repository."""
    ...  # fmt: off


class BlacklistTokenRepository(IBlacklistRepository, SQLModelRepository, ABC):
    """Repository for blacklist tokens."""
    model = BlacklistToken
