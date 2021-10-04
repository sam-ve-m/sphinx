# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from pymongo import MongoClient


class MongoDBInfrastructure:
    client: MongoClient = MongoClient(
        f"{config('MONGO_CONNECTION')}://{config('MONGODB_USER')}:{config('MONGODB_PASSWORD')}@{config('MONGODB_HOST')}:{config('MONGODB_PORT')}"
    )
