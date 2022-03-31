# OUTSIDE LIBRARIES
from copy import deepcopy

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
    async def create_view(cls, view: dict):
        if await cls.find_one({"_id": view["_id"]}):
            raise BadRequestError("common.register_exists")
        create = await cls.insert(view)
        return create

    @classmethod
    async def update_view(cls, view_id: str, view_update: dict):
        if not await cls.find_one({"_id": view_id}):
            raise BadRequestError("common.register_not_exists")
        update = await cls.update_one(old={"_id": view_id}, new=view_update)
        return update

    @classmethod
    async def delete_view(cls, view_id: str):
        if not await cls.find_one({"_id": view_id}):
            raise BadRequestError("common.register_not_exists")
        delete = await cls.delete_one({"_id": view_id})
        return delete

    @classmethod
    async def get_one_view(cls, view_id: str):
        view = await cls.find_one({"_id": view_id})
        return view

    @classmethod
    async def get_all_views(cls):
        views = await cls.find_all({})
        return views

    @classmethod
    async def link_feature_view(cls, feature_id: str, view_id: str):
        if not await cls.find_one({"_id": view_id}):
            raise BadRequestError("common.register_not_exists")
        link_feature_view_was_added = await cls.add_one_in_array(
            old={"_id": view_id},
            new={"features": feature_id},
            upsert=True
        )
        return link_feature_view_was_added

    @classmethod
    async def delete_link_feature_view(cls, feature_id: str, view_id: str):
        link_feature_view_was_deleted = await cls.delete_one_in_array(
            old={"_id": view_id},
            new={"features": feature_id},
            upsert=True
        )
        return link_feature_view_was_deleted

    @classmethod
    async def is_feature_linked_with_view(cls, feature_id: str, view_id: str) -> bool:
        view = await cls.find_one({
            "_id": view_id,
            "features": {
                "$elemMatch": {
                    "$eq": feature_id
                }
            }
        })
        return bool(view)

    @classmethod
    def exists(cls, view_id: str):
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.find_one(query={"_id": view_id}))
        value = current_event_loop.run_until_complete(task)
        return value is not None
