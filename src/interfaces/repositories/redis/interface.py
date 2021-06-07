from decouple import config
from redis import Redis
from typing import Optional
import pickle
from abc import ABC, abstractmethod

class IRedis:

    @abstractmethod
    def set(key: str, value: dict, redis: any, ttl: int = 0) -> bool:
       pass

    @abstractmethod
    def get(key: str, redis: any) -> Optional[dict]:
        pass

    @abstractmethod
    def get_keys(pattern: str, redis: any) -> Optional[list]:
       pass

    @abstractmethod
    def add_to_queue(key: str, value: tuple, redis: any) -> bool:
        pass

    @abstractmethod
    def get_from_queue(key: str, redis: any) -> Optional[dict]:
        pass
