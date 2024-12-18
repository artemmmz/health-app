"""Security module."""

import datetime
import logging
import uuid
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.settings import settings
from app.exceptions import InvalidTokenError
from app.utils.datetime import get_access_expires, get_now
from app.utils.enums import TokenType

# PASSWORD ENCRYPTION
context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Hash password.

    :param password: Plaintext password .
    :return: Hashed password.
    """
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hashed password.

    :param plain_password: Plaintext password.
    :param hashed_password: Hashed password.
    :return: Verified password or not.
    """
    return context.verify(plain_password, hashed_password)


# JWT
def encode_token(
    now: datetime.datetime = None,
    jti: str | uuid.UUID = None,
    expires_in: datetime.timedelta = None,
    **payload,
) -> str:
    """
    Encode JWT token.

    :param now: Current time in UTC.
    :param jti: Token identifier (by default UUID4).
    :param expires_in: Expiration time.
    :param payload: Token payload.
    :return: JWT token.
    """
    if now is None:
        now = get_now()
    if expires_in is None:
        expires_in = get_access_expires()
    if jti is None:
        jti = uuid.uuid4()
    if isinstance(jti, uuid.UUID):
        jti = str(jti)

    expires_at = now + expires_in
    payload = {
        **payload,
        'exp': expires_at,
        'iat': now,
        'jti': jti,
    }
    token = jwt.encode(
        payload, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_token(token: str, verify: bool = True) -> dict[str, Any]:
    """
    Decode JWT token.

    :param token: JWT token.
    :param verify: Need to verify token.
    :return: Token payload.
    """
    try:
        data = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            verify=verify,
        )
        return data
    except jwt.InvalidTokenError as e:
        logging.error(str(e))
        raise InvalidTokenError


def verify_token(token: str) -> bool:
    """
    Verify JWT token.

    :param token: JWT token.
    :return:
    """
    try:
        decode_token(token)
        return True
    except jwt.InvalidTokenError:
        return False


def create_access_token(
    user_id: int,
    username: str,
    jti: str | uuid.UUID = None,
    expires_in: datetime.timedelta = None,
    now: datetime.datetime = None,
) -> str:
    """
    Create JWT access token.

    :param user_id: User id.
    :param username: Username.
    :param jti: Token identifier (UUID4 by default).
    :param expires_in: Expiration time.
    :param now: Current time in UTC without timezone.
    :return: JWT access token.
    """
    return encode_token(
        sub=username,
        user_id=user_id,
        type=TokenType.ACCESS.value,
        jti=jti,
        expires_in=expires_in,
        now=now,
    )


def create_refresh_token(
    user_id: int,
    username: str,
    jti: str | uuid.UUID = None,
    expires_in: datetime.timedelta = None,
    now: datetime.datetime = None,
) -> str:
    """
    Create JWT refresh token.

    :param user_id: User id.
    :param username: Username.
    :param jti: Token identifier (UUID4 by default).
    :param expires_in: Expiration time.
    :param now: Current time in UTC without timezone.
    :return: JWT refresh token.
    """
    return encode_token(
        sub=username,
        user_id=user_id,
        type=TokenType.REFRESH.value,
        jti=jti,
        expires_in=expires_in,
        now=now,
    )
