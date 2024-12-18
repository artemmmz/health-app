from app.exceptions.base import AppError


class InvalidAuthCodeError(AppError):
    """Invalid authentication code error."""

    ...  # fmt: off
