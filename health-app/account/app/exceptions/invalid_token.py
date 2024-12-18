from app.exceptions.base import AppError


class InvalidTokenError(AppError):
    """Invalid or expired token error."""

    ...  # fmt: off
