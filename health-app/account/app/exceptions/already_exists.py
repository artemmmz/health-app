from app.exceptions.base import ModelError


class AlreadyExistsError(ModelError):
    """Already exists error for database models."""

    ...  # fmt: off
