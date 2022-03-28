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
        await feature_repository.create_feature(payload)
        create_feature_response = {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "requests.created",
        }
        return create_feature_response

    @staticmethod
    async def update(payload: dict, feature_id: str, feature_repository=FeatureRepository) -> dict:
        feature_update = deepcopy({"_id": feature_id})
        feature_update.update(payload.get("model"))
        if await feature_repository.update_feature(feature_id=feature_id, feature_update=feature_update):
            update_feature_response = {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
            return update_feature_response
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def delete(payload: dict, feature_repository=FeatureRepository) -> dict:
        if await feature_repository.delete_feature(payload.get("feature_id")):
            delete_feature_response = {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
            return delete_feature_response
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def get(payload: dict, feature_repository=FeatureRepository) -> dict:
        features = await feature_repository.get_features(payload)
        get_features_response = {
            "status_code": status.HTTP_200_OK,
            "payload": {"features": features},
        }
        return get_features_response
