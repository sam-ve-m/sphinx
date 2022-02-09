# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBInfrastructure:

    client = None

    @classmethod
    def _get_client(cls, mongo_connection, mongo_user, mongo_password, mongo_host, mongo_port):
        if cls.client is None:
            url = f"{mongo_connection}://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
            cls.client = AsyncIOMotorClient(url)

        return cls.client
