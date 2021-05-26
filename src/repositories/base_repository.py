from abc import ABC
from typing import Optional
from pymongo import MongoClient
from decouple import config
from pymongo.cursor import Cursor

class BaseRepository(ABC):

    client: MongoClient = (
            eval(config('MONGO_IS_SERVER')) == True and
            MongoClient(f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}/") or
            MongoClient(f"mongodb://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}/")
    )

    def __init__(self, database: str, collection: str) -> None:
        self.database = self.client[database]
        self.collection = self.database[collection]

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

    def find_one(self, query: dict) -> Optional[dict]:
        try:
            return self.collection.find_one(query)
        except Exception:
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
            self.collection.update_one(old, {'$set': new})
            return True
        except Exception:
            return False

    def delete_one(self, entity) -> bool:
        try:
            self.collection.delete_one(entity)
            return True
        except Exception:
            return False
