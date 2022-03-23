# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
import asyncio
import nest_asyncio

nest_asyncio.apply()

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class FeatureRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_FEATURE_COLLECTION")

    @classmethod
    def exists(cls, view_id: str):
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.find_one(query={"_id": view_id}))
        value = current_event_loop.run_until_complete(task)
        return value is not None
