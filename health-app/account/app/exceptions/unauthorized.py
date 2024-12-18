from app.exceptions.base import AppError


class UnauthorizedError(AppError):
    """Unauthorized error, user does not exist or inactive."""

    ...  # fmt: off
