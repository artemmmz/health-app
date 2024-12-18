from typing import Type, Optional

from app.models import BaseModel


class AppError(Exception):
    """Base class for app exceptions."""

    ...  # fmt: off


class ModelError(AppError):
    """Base class for model exceptions."""

    def __init__(self, model: Optional[Type[BaseModel] | str] = None):
        super().__init__()
        self.model = model
