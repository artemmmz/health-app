from app.exceptions import AppError
from app.utils.enums import TokenType


class InvalidTokenTypeError(AppError):
    """Invalid token type error."""

    def __init__(self, found: TokenType, expected: TokenType):
        super().__init__()
        self.found = found
        self.expected = expected
