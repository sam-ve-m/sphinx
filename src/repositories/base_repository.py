from abc import ABC, abstractmethod
from typing import Optional
from pymongo import MongoClient
from decouple import config


class BaseRepository(ABC):

    client: MongoClient = (
            eval(config('MONGO_IS_SERVER')) and
            MongoClient(f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_URI')}:{config('MONGODB_URI')}/") or
            MongoClient(f"mongodb://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_URI')}:{config('MONGODB_URI')}/")
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
        except Exception as e:
            return False

    def find_one(self, query: dict) -> Optional[dict]:
        try:
            return self.collection.find_one(query)
        except Exception as e:
            return None

    def find_more_then(self, query: dict) -> Optional[list]:
        try:
            return self.collection.find(query)
        except Exception as e:
            return None

    def find_all(self) -> Optional[list]:
        try:
            return self.collection.find()
        except Exception as e:
            return None

