# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from pymongo import MongoClient


class MongoDBInfrastructure:

    client = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            cls.client = MongoClient(
                f"{config('MONGO_CONNECTION')}://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}"
            )
        return cls.client
