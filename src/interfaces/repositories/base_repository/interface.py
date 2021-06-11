from abc import ABC, abstractmethod
from typing import Optional
from pymongo.cursor import Cursor

from src.repositories.cache.redis import RepositoryRedis


class IRepository(ABC):
    @abstractmethod
    def insert(self, data: dict) -> bool:
        pass

    @abstractmethod
    def insert_many(self, data: list) -> bool:
        pass

    @abstractmethod
    def find_one(self, query: dict, ttl: int = 0) -> Optional[dict]:
        pass

    @abstractmethod
    def find_more_than_equal_one(self, query: dict) -> Optional[Cursor]:
        pass

    @abstractmethod
    def find_all(self) -> Optional[Cursor]:
        pass

    @abstractmethod
    def update_one(self, old, new) -> bool:
        pass

    @abstractmethod
    def delete_one(self, entity) -> bool:
        pass
