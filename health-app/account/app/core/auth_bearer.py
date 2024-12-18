from fastapi import Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token
from app.exceptions import (
    InvalidAuthCodeError,
    InvalidAuthSchemeError,
    InvalidTokenError,
)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        """
        Get token payload by request.

        :param request: Request object.
        :return: Token payload.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )

        if not credentials:
            raise InvalidAuthCodeError
        if credentials.scheme != 'Bearer':
            raise InvalidAuthSchemeError

        token = credentials.credentials
        if not verify_token(token):
            raise InvalidTokenError
        return token
