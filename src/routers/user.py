from fastapi import APIRouter, Request
from src.routers.validators.base import Email, PIN, Name, View, OptionalPIN
from src.utils.jwt_utils import JWTHandler

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = APIRouter()


class UserSimple(Email, OptionalPIN, Name):
    pass


@router.post("/user", tags=["user"])
async def create_user(user: UserSimple, request: Request):
    return await BaseController.run(UserController.create, dict(user), request)


@router.post("/user_admin", tags=["user"])
async def create_admin(user: UserSimple, request: Request):
    return await BaseController.run(UserController.create_admin, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
async def forgot_password(user: Email, request: Request):
    return await BaseController.run(UserController.forgot_password, dict(user), request)


@router.put("/user", tags=["user"])
async def update_user_data(user: UserSimple, request: Request):
    # TODO: complete data
    return await BaseController.run(UserController.create_admin, dict(user), request)


@router.delete("/user", tags=["user"])
async def delete_user(request: Request):
    payload = JWTHandler.get_payload_from_request(request=request)
    return await BaseController.run(UserController.delete, payload, request)


@router.put("/user/change_password", tags=["user"])
async def change_user_password(pin: PIN, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "new_pin": dict(pin).get("pin"),
    }
    return await BaseController.run(UserController.change_password, payload, request)


@router.put("/user/view", tags=["user"])
async def change_user_view(view: View, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "new_view": dict(view).get("view"),
    }
    return await BaseController.run(UserController.change_view, payload, request)
