# STANDARD LIBS
import asyncio
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
        self.base_identifier = f"{database}:{collection}"
        self.database_name = database
        self.collection_name = collection

    async def get_collection(self):
        mongo_client = MongoDbBaseRepository._get_client()
        database = mongo_client[self.database_name]
        collection = database[self.collection_name]
        return collection

    async def insert(self, data: dict) -> bool:
        try:
            collection = await self.get_collection()
            result = await collection.insert_one(data)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    async def insert_many(self, data: list) -> bool:
        try:
            collection = await self.get_collection()
            await collection.insert_many(data)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            # TODO: Verificar esse return
            return False

    async def find_one(
        self, query: dict, ttl: int = 0, cache=RepositoryRedis
    ) -> Optional[dict]:
        try:
            collection = await self.get_collection()
            data = None

            has_ttl = ttl > 0  # pragma: no cover
            if has_ttl:  # pragma: no cover
                data = await self._get_from_cache(query=query, cache=cache)

            if not data:  # pragma: no cover
                data = await collection.find_one(query)

            if has_ttl and data is not None:  # pragma: no cover
                await self._save_cache(query=query, cache=cache, ttl=ttl, data=data)

            return data

        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise Exception("internal_error")

    async def find_more_than_equal_one(self, query: dict) -> Optional[Cursor]:
        try:
            collection = await self.get_collection()
            result = await collection.find(query)
            return result
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise Exception("internal_error")

    async def find_all(self, sort: tuple = None, limit: int = None) -> Optional[Cursor]:
        try:
            collection = await self.get_collection()
            query = collection.find()#.to_list(limit)
            if sort:
                query.sort(*sort)
            return await query.to_list(limit)
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise Exception("internal_error")

    async def find_one_with_specific_columns(
        self, query: dict, query_limit: dict
    ) -> Optional[dict]:
        try:
            collection = await self.get_collection()
            result = await collection.find_one(query, query_limit)
            return result
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise Exception("internal_error")

    async def update_one(self, old, new, ttl=60, cache=RepositoryRedis) -> bool:
        if not old or len(old) == 0:
            return False

        if not new or len(new) == 0:
            return False
        try:
            collection = await self.get_collection()
            Sindri.dict_to_primitive_types(new, types_to_ignore=[datetime])
            await collection.update_one(old, {"$set": new})
            if new.get("email"):
                await self._save_cache(
                    query={"_id": new.get("email")}, cache=cache, ttl=ttl, data=new
                )

            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            #TODO: Verificar esse return
            return False

    async def delete_one(self, entity, ttl=0, cache=RepositoryRedis) -> bool:
        try:
            collection = await self.get_collection()
            await collection.delete_one(entity)
            # TODO need to delete user cache ???
            if entity.get("email"):  # pragma: no cover
                await self._delete_cache(query={"_id": entity.get("email")}, cache=cache)
            return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            #TODO: Verificar esse return
            return False

    async def _get_from_cache(self, query: dict, cache=RepositoryRedis):
        if query is None:
            return None

        query_hash = hash_field(payload=query)

        #TODO: Check this await to redis sync
        cache_value = await cache.get(key=f"{self.base_identifier}:{query_hash}")
        if cache_value:
            return cache_value
        return None

    async def _save_cache(self, data: dict, query: dict, cache=RepositoryRedis, ttl: int = 0):

        # TODO shall have default time  ???
        # ttl = (ttl == 0) and 60 or ttl
        ttl = 60 if ttl == 0 else ttl  # pragma: no cover

        query_hash = hash_field(payload=query)
        await cache.set(
            key=f"{self.base_identifier}:{query_hash}",
            value=data,
            ttl=ttl,
        )

    @staticmethod
    async def _delete_cache(query: dict, cache=RepositoryRedis):
        query_hash = await hash_field(payload=query)
        await cache.delete(query_hash)
