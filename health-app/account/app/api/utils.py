from app.core.dependencies import BrokerAnnotation
from app.core.security import create_access_token, create_refresh_token
from app.models.token_models import Tokens
from app.models.user_models import User
from app.services.session_service import SessionService
from app.utils.datetime import get_now, get_access_expires


async def create_tokens_and_session(user: User, broker_uow: BrokerAnnotation):
    now = get_now()

    access_expires_in = get_access_expires()

    access_token = create_access_token(
        user_id=user.id_,
        username=user.username,
        expires_in=access_expires_in,
    )
    refresh_token = create_refresh_token(
        user_id=user.id_,
        username=user.username,
    )

    await SessionService.new_session(
        uow=broker_uow, access_token=access_token,
        token_expire=now + access_expires_in, user_id=user.id_,
        username=user.username
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token)