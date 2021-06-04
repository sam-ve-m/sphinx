from fastapi import APIRouter, Request, Response, UploadFile, File
from src.routers.validators.base import (
    Email,
    PIN,
    Name,
    View,
    OptionalPIN,
    Feature,
    TermFileType,
)
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from typing import Union

router = APIRouter()


class UserSimple(Email, Name, OptionalPIN):
    pass


@router.post("/user", tags=["user"])
def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.post("/user_admin", tags=["user"])
def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
def forgot_password(user: Email, request: Request):
    return BaseController.run(UserController.forgot_password, dict(user), request)


@router.put("/user", tags=["user"])
def update_user_data(user: UserSimple, request: Request):
    # TODO: complete data
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.delete("/user", tags=["user"])
def delete_user(request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    return BaseController.run(UserController.delete, thebes_answer_data, request)


@router.put("/user/change_password", tags=["user"])
def change_user_password(pin: PIN, request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    payload = {
        "thebes_answer": thebes_answer_data,
        "new_pin": dict(pin).get("pin"),
    }
    return BaseController.run(UserController.change_password, payload, request)


@router.put("/user/logout_all", tags=["user"])
def logout_all(request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    return BaseController.run(UserController.logout_all, thebes_answer_data, request)


@router.put("/user/view", tags=["user"])
def change_user_view(view: View, request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    payload = {
        "thebes_answer": thebes_answer_data,
        "new_view": dict(view).get("view"),
    }
    return BaseController.run(UserController.change_view, payload, request)


@router.put("/user/purchase", tags=["user"])
def add_features_to_user(feature: Feature, request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    payload = {
        "thebes_answer": thebes_answer_data,
        "feature": dict(feature).get("feature"),
    }
    return BaseController.run(UserController.add_feature, dict(payload), request)


@router.delete("/user/purchase", tags=["user"])
def remove_features_to_user(feature: Feature, request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    payload = {
        "thebes_answer": thebes_answer_data,
        "feature": dict(feature).get("feature"),
    }
    return BaseController.run(UserController.delete_feature, dict(payload), request)


@router.post("/user/self", tags=["user"])
async def save_user_self(
    request: Request, file_or_base64: Union[UploadFile, str] = File(...)
):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    if isinstance(file_or_base64, str) is False:
        file_or_base64 = await file_or_base64.read()
    payload = {
        "thebes_answer": thebes_answer_data,
        "file_or_base64": file_or_base64,
    }
    return BaseController.run(UserController.save_user_self, payload, request)


@router.put("/user/assign_term", tags=["user"])
async def assign_term(
    request: Request, file_type: TermFileType,
):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    payload = file_type.dict()
    payload.update({"thebes_answer": thebes_answer_data})
    return BaseController.run(UserController.assign_term, payload, request)
