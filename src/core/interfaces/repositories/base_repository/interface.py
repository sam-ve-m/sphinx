# STANDARD LIBS
from abc import ABC, abstractmethod
from typing import Optional

# OUTSIDE LIBRARIES
from pymongo.cursor import Cursor


# SPHINX


class IRepository(ABC):
    @abstractmethod
    def insert(self, data: dict) -> bool:
        pass

    @abstractmethod
    def find_one(self, query: dict, ttl: int = 0) -> Optional[dict]:
        pass

    @abstractmethod
    async def find_all(
        self,
        query: dict,
        project: dict = None,
    ) -> Optional[Cursor]:
        pass

    @abstractmethod
    def update_one(self, old, new, ttl: int = 0) -> bool:
        pass

    @abstractmethod
    def delete_one(self, entity, ttl: int = 0) -> bool:
        pass
