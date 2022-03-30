# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
import asyncio
import nest_asyncio

from src.exceptions.exceptions import BadRequestError

nest_asyncio.apply()

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class FeatureRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_FEATURE_COLLECTION")

    @classmethod
    async def create_feature(cls, payload: dict):
        payload.update({"_id": payload["name"]})
        if await cls.find_one({"_id": payload.get("_id")}):
            raise BadRequestError("common.register_exists")
        await cls.insert(payload)

    @classmethod
    async def update_feature(cls, feature_id: str, feature_update: dict):
        if not await cls.find_one({"_id": feature_id}):
            raise BadRequestError("common.register_not_exists")
        updated = await cls.update_one(old={"_id": feature_id}, new=feature_update)
        return updated

    @classmethod
    async def delete_feature(cls, feature_id: str):
        if not await cls.find_one({"_id": feature_id}):
            raise BadRequestError("common.register_not_exists")
        delete = await cls.delete_one({"_id": feature_id})
        return delete

    @classmethod
    async def get_features(cls, payload: dict):
        features = await cls.find_all(payload)
        return features

    @classmethod
    def feature_exists(cls, feature_id: str) -> bool:
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.find_one(query={"_id": feature_id}))
        value = current_event_loop.run_until_complete(task)
        return value is not None
