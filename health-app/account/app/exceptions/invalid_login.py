from app.exceptions import AppError


class InvalidLoginError(AppError):
    """Username or password error. Use only in signin endpoint."""

    ...  # fmt: off
