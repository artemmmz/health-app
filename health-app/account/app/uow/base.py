from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """Interface for unit-of-work."""

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
