# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.repositories.view.repository import ViewRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.core.interfaces.services.view.interface import IView


class ViewService(IView):
    @staticmethod
    async def create(payload: dict, view_repository=ViewRepository) -> dict:
        payload.update({"_id": payload["name"], "features": list()})
        if await view_repository.find_one(payload) is not None:
            raise BadRequestError("common.register_exists")
        if await view_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "requests.created",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def update(payload: dict, view_repository=ViewRepository) -> dict:
        display_name = payload.get("model").get("display_name")
        old = await view_repository.find_one({"_id": payload.get("view_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["display_name"] = display_name
        if await view_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def delete(payload: dict, view_repository=ViewRepository) -> dict:
        view_id = payload.get("view_id")
        old = await view_repository.find_one({"_id": view_id})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if await view_repository.delete_one({"_id": view_id}):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def link_feature(payload: dict, view_repository=ViewRepository) -> dict:
        feature_id = payload.get("feature_id")
        old = await view_repository.find_one({"_id": payload.get("view_id")})
        if old and feature_id not in old.get("features"):
            new = deepcopy(old)
            new["features"].append(feature_id)
            if await view_repository.update_one(old=old, new=new):
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "requests.updated",
                }
            else:
                raise InternalServerError("common.process_issue")
        return {
            # "status_code": status.HTTP_304_NOT_MODIFIED,
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.not_modified",
        }

    @staticmethod
    async def delink_feature(payload: dict, view_repository=ViewRepository) -> dict:
        feature_id = payload.get("feature_id")
        old = await view_repository.find_one({"_id": payload.get("view_id")})
        if old and feature_id in old.get("features"):
            new = deepcopy(old)
            new["features"].remove(feature_id)
            if await view_repository.update_one(old=old, new=new):
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "requests.updated",
                }
            else:
                raise InternalServerError("common.process_issue")
        return {
            # "status_code": status.HTTP_304_NOT_MODIFIED,
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.not_modified",
        }

    @staticmethod
    async def get_view(payload: dict, view_repository=ViewRepository) -> dict:
        view = await view_repository.find_one({"_id": payload.get("view_id")})
        if view is None:
            raise BadRequestError("common.register_not_exists")
        return {"status_code": status.HTTP_200_OK, "payload": view}

    @staticmethod
    async def get(payload: dict, view_repository=ViewRepository) -> dict:
        views = await view_repository.find_all()
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"views": views},
        }
