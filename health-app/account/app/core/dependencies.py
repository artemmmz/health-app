"""Dependencies module."""

import uuid
from typing import Annotated, Dict, Any

from fastapi import Depends

from app.core.auth_bearer import JWTBearer
from app.core.security import decode_token
from app.exceptions import (
    ForbiddenError,
    UnauthorizedError,
    NoResultError,
    InvalidTokenError,
    InvalidTokenTypeError,
)
from app.kafka.app import app
from app.models.role_models import UserRole
from app.models.user_models import User
from app.services import UserService, TokenService, RoleService
from app.uow.broker import IBrokerUnitOfWork, KafkaUOW
from app.uow.database import SQLAlchemyUOW, IDatabaseUnitOfWork
from app.uow.inmemory import IInMemoryUnitOfWork, RedisUOW
from app.utils.enums import Role, TokenType


# UOW Section
def create_db_uow() -> IDatabaseUnitOfWork:
    """Create and initialize Unit Of Work instance."""
    return SQLAlchemyUOW()


def create_inmemory_uow() -> IInMemoryUnitOfWork:
    """Create and initialize InMemory Unit Of Work instance."""
    return RedisUOW()


def create_broker_uow() -> IBrokerUnitOfWork:
    """Create and initialize Kafka Broker Unit Of Work instance."""
    return KafkaUOW(app)


DBDep = Depends(create_db_uow)
DBAnnotation = Annotated[IDatabaseUnitOfWork, DBDep]

InMemoryDep = Depends(create_inmemory_uow)
InMemoryAnnotation = Annotated[IInMemoryUnitOfWork, InMemoryDep]

BrokerDep = Depends(create_broker_uow)
BrokerAnnotation = Annotated[IBrokerUnitOfWork, BrokerDep]


# Authentication Section
async def get_current_token_payload(
    inmemory: InMemoryAnnotation, token: str = Depends(JWTBearer())
):
    """
    Check token and get token payload.

    :param inmemory: In-memory Unit of Work instance.
    :param token: JWT Token.
    :return: Token payload.
    """
    payload = decode_token(token)
    token_id = uuid.UUID(payload['jti'])
    in_blacklist = await TokenService.check_blacklist_token(inmemory, token_id)
    if in_blacklist:
        raise InvalidTokenError
    return payload


TokenDep = Depends(get_current_token_payload)
TokenAnnotation = Annotated[Dict[str, Any], TokenDep]


async def __get_current_user(
    uow: DBAnnotation, payload: Dict[str, Any], by_token: TokenType
) -> User:
    """Get current user."""
    if payload is None:
        raise UnauthorizedError
    if payload['type'] != by_token.value:
        raise InvalidTokenTypeError
    try:
        user = await UserService.get_user_by_id(uow, payload['user_id'])
        return user
    except NoResultError:
        raise UnauthorizedError


async def get_current_user(
    uow: DBAnnotation, payload: TokenAnnotation
) -> User:
    """
    Get current user.

    :param uow: Unit Of Work instance.
    :param payload: Token payload.
    :return: Current active user.
    """
    return await __get_current_user(uow, payload, TokenType.ACCESS)


async def get_current_user_by_refresh(
    uow: DBAnnotation, payload: TokenAnnotation
) -> User:
    """
    Get current user by refresh token.

    :param uow: Unit Of Work instance.
    :param payload: Token payload.
    :return: Current active user.
    """
    return await __get_current_user(uow, payload, TokenType.REFRESH)


UserDep = Depends(get_current_user)
UserAnnotation = Annotated[User, UserDep]

UserRefreshDep = Depends(get_current_user_by_refresh)
UserRefreshAnnotation = Annotated[User, UserRefreshDep]


async def get_current_admin(uow: DBAnnotation, user: UserAnnotation) -> User:
    """
    Get current admin user.

    :param uow: Unit of work instance.
    :param user: User instance from dependency.
    :return: Current active admin user.
    """
    user_roles: list[UserRole] = await RoleService.get_roles(uow, user.id_)
    roles = [role.role for role in user_roles]
    if Role.ADMIN not in roles:
        raise ForbiddenError
    return user


AdminDep = Depends(get_current_admin)
