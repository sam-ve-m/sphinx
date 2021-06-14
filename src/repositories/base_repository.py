# STANDARD LIBS
from typing import Optional
import logging
from enum import Enum

# OUTSIDE LIBRARIES
from decouple import config
from pymongo.cursor import Cursor
from pymongo import MongoClient

# SPHINX
from src.repositories.cache.redis import RepositoryRedis
from src.utils.genarate_id import hash_field
from src.interfaces.repositories.base_repository.interface import IRepository


class BaseRepository(IRepository):
    client: MongoClient = (
        eval(config("PRODUCTION")) is True
        and MongoClient(
            f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}"
        )
        or MongoClient(
            f"mongodb://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}"
        )
    )

    def __init__(self, database: str, collection: str) -> None:
        self.base_identifier = f"{database}:{collection}"
        self.database = self.client[database]
        self.collection = self.database[collection]

    def insert(self, data: dict) -> bool:
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def insert_many(self, data: list) -> bool:
        try:
            self.collection.insert_many(data)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def find_one(
        self, query: dict, ttl: int = 0, cache=RepositoryRedis
    ) -> Optional[dict]:
        try:
            if ttl > 0:
                value = self._get_from_cache(query=query, cache=cache, ttl=ttl)
            else:
                value = self.collection.find_one(query)
            return value
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return None

    def find_more_than_equal_one(self, query: dict) -> Optional[Cursor]:
        try:
            return self.collection.find(query)
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return None

    def find_all(self) -> Optional[Cursor]:
        try:
            return self.collection.find()
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return None

    def update_one(self, old, new) -> bool:
        if old is None or new is None:
            return False
        self.normalize_enum_types(payload=new)
        try:
            self.collection.update_one(old, {"$set": new})
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def delete_one(self, entity) -> bool:
        try:
            self.collection.delete_one(entity)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def normalize_enum_types(self, payload: dict):
        for key in payload:
            if isinstance(payload[key], Enum):
                payload[key] = payload[key].value
            elif type(payload[key]) == dict:
                self.normalize_enum_types(payload=payload[key])

    def _get_from_cache(self, query: dict, ttl: int, cache=RepositoryRedis):
        query_hash = hash_field(payload=query)
        if query_hash:
            cache_value = cache.get(key=f"{self.base_identifier}:{query_hash}")
            if cache_value:
                return cache_value
            else:
                cache_value = self.collection.find_one(query)
                cache.set(
                    key=f"{self.base_identifier}:{query_hash}",
                    value=cache_value,
                    ttl=ttl,
                )
            return cache_value
