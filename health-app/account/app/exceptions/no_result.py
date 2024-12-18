from app.exceptions.base import ModelError


class NoResultError(ModelError):
    """No result in database error."""

    ...  # fmt: off
