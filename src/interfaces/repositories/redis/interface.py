# STANDARD LIBS
from abc import ABC, abstractmethod
from typing import Optional


class IRedis(ABC):

    @staticmethod
    @abstractmethod
    def set(key: str, value: dict, redis: any, ttl: int = 0) -> bool:
       pass

    @staticmethod
    @abstractmethod
    def get(key: str, redis: any) -> Optional[dict]:
        pass

    @staticmethod
    @abstractmethod
    def get_keys(pattern: str, redis: any) -> Optional[list]:
       pass

    @staticmethod
    @abstractmethod
    def add_to_queue(key: str, value: tuple, redis: any) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def get_from_queue(key: str, redis: any) -> Optional[dict]:
        pass
