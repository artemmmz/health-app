import datetime

from app.kafka.models import Session
from app.uow.broker import IBrokerUnitOfWork
from app.utils.enums import SessionAction


class SessionService:
    @staticmethod
    async def new_session(
            uow: IBrokerUnitOfWork, access_token: str,
            token_expire: datetime.datetime, user_id: int, username: str,
            token_type: str = 'Bearer'
    ):
        instance = Session(
            action=SessionAction.CREATE,
            access_token=access_token, token_type=token_type,
            expires_in=token_expire, user_id=user_id, username=username
        )
        async with uow:
            return await uow.session_repository.send(value=instance)

    @staticmethod
    async def terminate_session(
            uow: IBrokerUnitOfWork, access_token: str,
    ):
        instance = Session(action=SessionAction.TERMINATE, access_token=access_token)
        async with uow:
            return await uow.session_repository.send(value=instance)
