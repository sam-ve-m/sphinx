# STANDARD LIBS
from typing import Optional
import logging
from datetime import datetime

# OUTSIDE LIBRARIES
from pymongo.cursor import Cursor
from nidavellir.src.uru import Sindri

# Sphinx
from src.infrastructures.env_config import config
from src.core.interfaces.repositories.base_repository.interface import IRepository
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from src.repositories.cache.redis import RepositoryRedis
from src.domain.model_decorator.generate_id import hash_field


class MongoDbBaseRepository(MongoDBInfrastructure, IRepository):
    def __init__(self, database: str, collection: str) -> None:
        mongo_client = MongoDbBaseRepository._get_client()
        self.base_identifier = f"{database}:{collection}"
        self.database = mongo_client[database]
        self.collection = self.database[collection]

    def insert(self, data: dict) -> bool:
        try:
            result = self.collection.insert_one(data)
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
            data = None

            has_ttl = ttl > 0  # pragma: no cover
            if has_ttl:  # pragma: no cover
                data = self._get_from_cache(query=query, cache=cache)

            if not data:  # pragma: no cover
                data = self.collection.find_one(query)

            if has_ttl and data is not None:  # pragma: no cover
                self._save_cache(query=query, cache=cache, ttl=ttl, data=data)

            return data

        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return

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
            return

    def find_one_with_specific_columns(
        self, query: dict, query_limit: dict
    ) -> Optional[dict]:
        try:
            return self.collection.find_one(query, query_limit)
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return None

    def update_one(self, old, new, ttl=60, cache=RepositoryRedis) -> bool:
        if not old or len(old) == 0:
            return False

        if not new or len(new) == 0:
            return False
        try:
            Sindri.dict_to_primitive_types(new, types_to_ignore=[datetime])
            self.collection.update_one(old, {"$set": new})
            if new.get("email"):
                self._save_cache(
                    query={"_id": new.get("email")}, cache=cache, ttl=ttl, data=new
                )

            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def delete_one(self, entity, ttl=0, cache=RepositoryRedis) -> bool:
        try:
            self.collection.delete_one(entity)
            # TODO need to delete user cache ???
            if entity.get("email"):  # pragma: no cover
                self._delete_cache(query={"_id": entity.get("email")}, cache=cache)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    def _get_from_cache(self, query: dict, cache=RepositoryRedis):
        if query is None:
            return

        query_hash = hash_field(payload=query)
        cache_value = cache.get(key=f"{self.base_identifier}:{query_hash}")
        if cache_value:
            return cache_value

        return

    def _save_cache(self, data: dict, query: dict, cache=RepositoryRedis, ttl: int = 0):

        # TODO shall have default time  ???
        # ttl = (ttl == 0) and 60 or ttl
        ttl = 60 if ttl == 0 else ttl  # pragma: no cover

        query_hash = hash_field(payload=query)
        cache.set(
            key=f"{self.base_identifier}:{query_hash}",
            value=data,
            ttl=ttl,
        )

    @staticmethod
    def _delete_cache(query: dict, cache=RepositoryRedis):
        query_hash = hash_field(payload=query)
        cache.delete(query_hash)