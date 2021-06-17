# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.repositories.view.repository import ViewRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, generate_list
from src.interfaces.services.view.interface import IView


class ViewService(IView):
    @staticmethod
    def create(payload: dict, view_repository=ViewRepository()) -> dict:
        payload = generate_id("name", payload)
        payload = generate_list("features", payload)
        if view_repository.find_one(payload) is not None:
            raise BadRequestError("common.register_exists")
        if view_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "requests.created",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def update(payload: dict, view_repository=ViewRepository()) -> dict:
        display_name = payload.get("model").get("display_name")
        old = view_repository.find_one({"_id": payload.get("view_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new["display_name"] = display_name
        if view_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def delete(payload: dict, view_repository=ViewRepository()) -> dict:
        view_id = payload.get("view_id")
        old = view_repository.find_one({"_id": view_id})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if view_repository.delete_one({"_id": view_id}):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def link_feature(payload: dict, view_repository=ViewRepository()) -> dict:
        feature_id = payload.get("feature_id")
        old = view_repository.find_one({"_id": payload.get("view_id")})
        if old:
            features = old.get("features")
            if features is None:
                raise InternalServerError("common.process_issue")
            if feature_id not in features:
                new = dict(old)
                new.get("features").append(feature_id)
                if view_repository.update_one(old=old, new=new) is False:
                    raise InternalServerError("common.process_issue")
            return {"status_code": status.HTTP_200_OK, "message_key": "requests.updated"}
        return {"status_code": status.HTTP_304_NOT_MODIFIED, "message_key": "requests.not_modified"}

    @staticmethod
    def get_view(payload: dict, view_repository=ViewRepository()) -> dict:
        view = view_repository.find_one({"_id": payload.get("view_id")})
        if view is None:
            raise BadRequestError("common.register_not_exists")
        return {"status_code": status.HTTP_200_OK, "payload": view}
