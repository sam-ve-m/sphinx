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
        view_id = payload["name"]
        payload.update({"_id": view_id})
        create_view_succeeded = await view_repository.create_view(view=payload)
        if create_view_succeeded:
            create_view_response = {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "requests.created",
            }
            return create_view_response
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def update(payload: dict, view_repository=ViewRepository) -> dict:
        view_id = payload.get("view_id")
        view_update = deepcopy({"_id": view_id})
        view_update.update(payload.get("model"))
        view_update_succeeded = await view_repository.update_view(view_id=view_id, view_update=view_update)
        if view_update_succeeded:
            update_view_response = {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
            return update_view_response
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def delete(payload: dict, view_repository=ViewRepository) -> dict:
        view_id = payload.get("view_id")
        delete_view_succeeded = await view_repository.delete_view(view_id)
        if delete_view_succeeded:
            delete_view_response = {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
            return delete_view_response
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def link_feature(payload: dict, view_repository=ViewRepository) -> dict:
        feature_id = payload.get("feature_id")
        view_id = payload.get("view_id")
        is_already_linked = await view_repository.is_feature_linked_with_view(feature_id=feature_id, view_id=view_id)
        if is_already_linked:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.not_modified",
            }
        feature_was_linked = await view_repository.link_feature_view(feature_id=feature_id, view_id=view_id)
        if feature_was_linked:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def delete_link_feature(payload: dict, view_repository=ViewRepository) -> dict:
        feature_id = payload.get("feature_id")
        view_id = payload.get("view_id")
        is_already_linked = await view_repository.is_feature_linked_with_view(feature_id=feature_id, view_id=view_id)
        if not is_already_linked:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.not_modified",
            }

        feature_was_delete_linked = await view_repository.delete_link_feature_view(feature_id=feature_id, view_id=view_id)
        if feature_was_delete_linked:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.deleted",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def get_view(payload: dict, view_repository=ViewRepository) -> dict:
        view_id = payload.get("view_id")
        view = await view_repository.get_one_view(view_id)
        if view is None:
            raise BadRequestError("common.register_not_exists")
        get_one_view_response = {"status_code": status.HTTP_200_OK, "payload": view}
        return get_one_view_response

    @staticmethod
    async def get(view_repository=ViewRepository) -> dict:
        views = await view_repository.get_all_views()
        get_all_views_response = {
            "status_code": status.HTTP_200_OK,
            "payload": {"views": views},
        }
        return get_all_views_response
