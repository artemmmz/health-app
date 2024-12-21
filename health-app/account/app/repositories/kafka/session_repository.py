from abc import ABC

from app.kafka.models import Session
from app.repositories.kafka.base import KafkaRepository


class ISessionRepository(KafkaRepository, ABC):
    ...


class SessionRepository(ISessionRepository, ABC):
    topic_name = 'sessions'
    topic_value_type = Session
