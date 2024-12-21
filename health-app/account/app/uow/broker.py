from abc import ABC
from typing import Self, Optional

from faust import App

from app.repositories.kafka.session_repository import ISessionRepository, SessionRepository


class IBrokerUnitOfWork(ABC):
    session_repository: Optional[ISessionRepository]


class KafkaUOW(IBrokerUnitOfWork):
    def __init__(self, app: App):
        self.app = app

    async def __aenter__(self) -> Self:
        self.session_repository = SessionRepository(self.app)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session_repository = None
