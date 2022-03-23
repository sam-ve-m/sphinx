# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.core.interfaces.services.feature.interface import IFeature
from src.repositories.feature.repository import FeatureRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError


class FeatureService(IFeature):
    @staticmethod
    async def create(payload: dict, feature_repository=FeatureRepository) -> dict:
        payload.update({"_id": payload["name"]})
        if await feature_repository.find_one({"_id": payload.get("_id")}):
            raise BadRequestError("common.register_exists")
        if await feature_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "requests.created",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def update(payload: dict, feature_repository=FeatureRepository) -> dict:
        old = await feature_repository.find_one({"_id": payload.get("feature_id")})
        if not old:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new.update(payload.get("model"))
        if await feature_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def delete(payload: dict, feature_repository=FeatureRepository) -> dict:
        feature_id = payload.get("feature_id")
        if await feature_repository.delete_one({"_id": feature_id}):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def get(payload: dict, feature_repository=FeatureRepository) -> dict:
        features = await feature_repository.find_all()
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"features": features},
        }
