from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = APIRouter()


class UserSimple(BaseModel):
    name: str
    email: str
    pin: Optional[int]


class UserUpdateView(BaseModel):
    view: str


class UserUpdatePassword(BaseModel):
    new_password: str


class UserComplete(BaseModel):
    name: str
    view: str


class ForgotPassword(BaseModel):
    email: str


@router.post("/user", tags=["user"])
async def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.post("/user/admin", tags=["user"])
async def create_admin_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.put("/user", tags=["user"])
async def update_user_data(user: UserComplete, request: Request):
    # TODO: complete data
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.delete("/user", tags=["user"])
async def delete_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.delete, dict(user), request)


@router.put("/user/change_password", tags=["user"])
async def change_user_password(user: UserUpdatePassword, request: Request):
    return BaseController.run(UserController.change_password, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
async def change_user_forgot_password(user: ForgotPassword, request: Request):
    return BaseController.run(UserController.forgot_password, dict(user), request)


@router.put("/user/view", tags=["user"])
async def change_user_view(user: UserUpdateView, request: Request):
    return BaseController.run(UserController.change_view, dict(user), request)
