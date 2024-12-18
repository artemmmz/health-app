from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """Abstract repository for working with data."""

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        raise NotImplementedError
