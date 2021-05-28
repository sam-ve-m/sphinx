from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from src.utils.jwt_utils import JWTHandler

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = APIRouter()


class UserSimple(BaseModel):
    name: str
    email: str
    pin: Optional[int]


class UserUpdateView(BaseModel):
    new_view: str


class UserUpdatePin(BaseModel):
    new_pin: str


class UserComplete(BaseModel):
    name: str
    view: str


class ForgotPassword(BaseModel):
    email: str


@router.post("/user", tags=["user"])
async def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.post("/user_admin", tags=["user"])
async def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
async def forgot_password(user: ForgotPassword, request: Request):
    return BaseController.run(UserController.forgot_password, dict(user), request)


@router.put("/user", tags=["user"])
async def update_user_data(user: UserComplete, request: Request):
    # TODO: complete data
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.delete("/user", tags=["user"])
async def delete_user(request: Request):
    payload = JWTHandler.get_payload_from_request(request=request)
    return BaseController.run(UserController.delete, payload, request)


@router.put("/user/change_password", tags=["user"])
async def change_user_password(user: UserUpdatePin, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "new_pin": dict(user).get("new_pin"),
    }
    return BaseController.run(UserController.change_password, payload, request)


@router.put("/user/view", tags=["user"])
async def change_user_view(user: UserUpdateView, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "new_view": dict(user).get("new_view"),
    }
    return BaseController.run(UserController.change_view, payload, request)
