# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.core.interfaces.services.feature.interface import IFeature
from src.repositories.feature.repository import FeatureRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.domain.model_decorator.generate_id import generate_id


class FeatureService(IFeature):
    @staticmethod
    def create(payload: dict, feature_repository=FeatureRepository()) -> dict:
        payload = generate_id("name", payload)
        if feature_repository.find_one({"_id": payload.get("_id")}):
            raise BadRequestError("common.register_exists")
        if feature_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "requests.created",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def update(payload: dict, feature_repository=FeatureRepository()) -> dict:
        display_name = payload.get("model").get("display_name")
        old = feature_repository.find_one({"_id": payload.get("feature_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["display_name"] = display_name
        if feature_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def delete(payload: dict, feature_repository=FeatureRepository()) -> dict:
        feature_id = payload.get("feature_id")
        if feature_repository.delete_one({"_id": feature_id}):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
        else:
            raise InternalServerError("common.process_issue")
