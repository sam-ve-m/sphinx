# STANDARD LIBS
from abc import ABC, abstractmethod
from typing import Optional


class IRedis(ABC):
    @staticmethod
    @abstractmethod
    async def set(key: str, value: dict, ttl: int = 0) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def get(key: str) -> Optional[dict]:
        pass

    @staticmethod
    @abstractmethod
    async def get_keys(pattern: str) -> Optional[list]:
        pass

    @staticmethod
    @abstractmethod
    async def add_to_queue(key: str, value: tuple) -> bool:
        pass

    @staticmethod
    @abstractmethod
    async def get_from_queue(key: str) -> Optional[dict]:
        pass
