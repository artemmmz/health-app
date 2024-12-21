import datetime
from abc import ABC, abstractmethod
from typing import Optional, Any, Type

from faust import App, Record


class IKafkaRepository(ABC):
    @abstractmethod
    async def send(self, value: str | dict | list, key: Optional[str | bytes] = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def consume(self, timeout: Optional[datetime.timedelta | float | int | str] = None):
        raise NotImplementedError


class KafkaRepository(IKafkaRepository, ABC):
    topic_name: str
    topic_value_type: Type[Record] | Any

    def __init__(self, application: App):
        self.app = application
        self.topic = application.topic(self.topic_name, value_type=self.topic_value_type)

    async def send(
            self, value: Type[Record] | Any, key: Optional[str | bytes] = None
    ):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return await self.topic.send(value=value, key=key)

    async def consume(self, timeout: Optional[datetime.timedelta | float | int | str] = None):
        return await self.topic.get(timeout=timeout)

