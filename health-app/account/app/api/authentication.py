import uuid

from fastapi import APIRouter

from app.api.utils import create_tokens_and_session
from app.core.dependencies import (
    DBAnnotation,
    TokenAnnotation,
    UserRefreshDep,
    InMemoryAnnotation, BrokerAnnotation,
)
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
)
from app.exceptions import InvalidLoginError, NoResultError
from app.models.token_models import (
    Tokens,
    TokenPayload,
)
from app.models.user_models import UserAdd, Authentication
from app.services import UserService, TokenService, RoleService
from app.services.session_service import SessionService
from app.utils.datetime import get_now, get_access_expires, get_refresh_expires
from app.utils.enums import TokenStatus, Role

router = APIRouter()


@router.post('/signup')
async def signup(data: UserAdd, uow: DBAnnotation, broker_uow: BrokerAnnotation) -> Tokens:
    """Register a new user."""
    password = data.password1.get_secret_value()
    creation_data = data.model_dump(exclude={'password1', 'password2'})
    creation_data['password'] = password
    user = await UserService.add_user(uow, creation_data)
    await RoleService.add_role(uow, user.id_, Role.USER)

    return await create_tokens_and_session(user, broker_uow)


@router.post('/signin')
async def signin(data: Authentication, uow: DBAnnotation, broker_uow: BrokerAnnotation) -> Tokens:
    """Authenticate a user."""
    try:
        user = await UserService.get_user(uow, username=data.username)
    except NoResultError:
        raise InvalidLoginError
    if not verify_password(data.password.get_secret_value(), user.password):
        raise InvalidLoginError

    return await create_tokens_and_session(user, broker_uow)


@router.put(
    '/signout',
    responses={
        '200': {
            'content': {'application/json': {'example': {'status': 'ok'}}}
        }
   },
    dependencies=[UserRefreshDep])
async def signout(
    token_payload: TokenAnnotation, inmemory: InMemoryAnnotation, broker: BrokerAnnotation
):
    """Sign out a user."""
    token_id = uuid.UUID(token_payload['jti'])
    await TokenService.blacklist_token(inmemory, token_id)
    return {'status': 'ok'}


@router.get('/validate')
async def validate(
    access_token: str, inmemory: InMemoryAnnotation
) -> TokenPayload:
    """Introspection the token."""
    decoded_token = decode_token(access_token, verify=False)
    token_status = TokenStatus.ACTIVE
    if not verify_token(access_token):
        token_status = TokenStatus.EXPIRED
    is_blacklisted = await TokenService.check_blacklist_token(
        inmemory, decoded_token['jti']
    )
    if is_blacklisted:
        token_status = TokenStatus.BLACKLISTED
    return TokenPayload(**decoded_token, status=token_status)


@router.post(
    '/access', response_model_exclude_none=True, dependencies=[UserRefreshDep]
)
async def access(refresh_payload: TokenAnnotation, broker: BrokerAnnotation) -> Tokens:
    """
    Get new access token from refresh token
    (need refresh token in header).
    """
    now = get_now()
    expires_in = get_access_expires()
    expires_at = now + expires_in
    access_token = create_access_token(
        refresh_payload['user_id'],
        refresh_payload['sub'],
        refresh_payload['jti'],
        expires_in=expires_in,
        now=now,
    )

    await SessionService.new_session(
        broker, access_token, expires_at,
        refresh_payload['user_id'], refresh_payload['sub']
    )
    result = Tokens(access_token=access_token, expires_at=expires_at)
    return result


@router.post('/refresh', dependencies=[UserRefreshDep])
async def refresh(refresh_payload: TokenAnnotation, broker: BrokerAnnotation) -> Tokens:
    """Get a new pair of tokens (need refresh token in header)."""
    token_id = uuid.uuid4()
    now = get_now()
    refresh_expires_in = get_refresh_expires()
    access_expires_in = get_access_expires()

    access_token = create_access_token(
        refresh_payload['user_id'],
        refresh_payload['sub'],
        token_id,
        expires_in=access_expires_in,
        now=now,
    )
    refresh_token = create_refresh_token(
        refresh_payload['user_id'],
        refresh_payload['sub'],
        token_id,
        expires_in=refresh_expires_in,
        now=now,
    )

    await SessionService.new_session(
        broker, access_token, now + access_expires_in,
        refresh_payload['user_id'], refresh_payload['sub']
    )

    result = Tokens(access_token=access_token, refresh_token=refresh_token)
    return result
