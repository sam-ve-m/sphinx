# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
import asyncio
import nest_asyncio
from src.exceptions.exceptions import BadRequestError

nest_asyncio.apply()

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class ViewRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_VIEW_COLLECTION")

    @classmethod
    async def create_view(cls, payload: dict):
        payload.update({"_id": payload["name"], "features": list()})
        if await cls.find_one(payload) is not None:
            raise BadRequestError("common.register_exists")
        create = await cls.insert(payload)
        return create

    # @classmethod
    # async def update_view(cls, view_id: str, view_update: dict):
    #     if not await cls.find_one({"_id": view_id}):
    #         raise BadRequestError("common.register_not_exists")
    #     updated = await cls.update_one(old={"_id": view_id}, new=view_update)
    #     return updated

    @classmethod
    def exists(cls, view_id: str):
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.find_one(query={"_id": view_id}))
        value = current_event_loop.run_until_complete(task)
        return value is not None
