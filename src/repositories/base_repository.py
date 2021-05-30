from abc import ABC
from typing import Optional
from pymongo import MongoClient
from decouple import config
from pymongo.cursor import Cursor

from src.repositories.cache.redis import RepositoryRedis
from src.utils.genarate_id import hash_field


class BaseRepository(ABC):
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
        self.base_identifier = f'{database}:{collection}'
        self.database = self.client[database]
        self.collection = self.database[collection]

    @staticmethod
    def get_cache():
        pass

    def insert(self, data: dict) -> bool:
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            return False

    def insert_many(self, data: list) -> bool:
        try:
            self.collection.insert_many(data)
            return True
        except Exception:
            return False

    def find_one(self, query: dict, ttl: int = 0, cache=RepositoryRedis) -> Optional[dict]:
        try:
            if ttl > 0:
                query_hash = hash_field(payload=query)
                cache_value = cache.get(key=f'{self.base_identifier}:{query_hash}')
                if cache_value:
                    value = cache_value
                else:
                    value = self.collection.find_one(query)
                    cache.set(key=f'{self.base_identifier}:{query_hash}', value=value, ttl=ttl)
            else:
                value = self.collection.find_one(query)
            return value
        except Exception as e:
            print(e)
            return None


    def find_more_than_equal_one(self, query: dict) -> Optional[Cursor]:
        try:
            return self.collection.find(query)
        except Exception:
            return None

    def find_all(self) -> Optional[Cursor]:
        try:
            return self.collection.find()
        except Exception:
            return None

    def update_one(self, old, new) -> bool:
        try:
            self.collection.update_one(old, {"$set": new})
            return True
        except Exception:
            return False

    def delete_one(self, entity) -> bool:
        try:
            self.collection.delete_one(entity)
            return True
        except Exception:
            return False
