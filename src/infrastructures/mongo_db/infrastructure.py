# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBInfrastructure:

    client = None

    @classmethod
    def _get_client(cls):
        mongo_connection = config("MONGO_CONNECTION")
        mongo_user = config("MONGODB_USER")
        mongo_password = config("MONGODB_PASSWORD")
        mongo_host = config("MONGODB_HOST")
        mongo_port = config("MONGODB_PORT")
        if cls.client is None:
            url = f"{mongo_connection}://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
            cls.client = AsyncIOMotorClient(url)

        return cls.client
