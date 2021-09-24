# OUTSIDE LIBRARIES
from fastapi import Depends, Request

# SPHINX
from src.routers.validators.base import (
    Email,
    OptionalPIN,
    NickName,
)
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.public import PublicRouter

router = PublicRouter.instance()

# TODO: remover from here


class UserSimple(Email, NickName, OptionalPIN):
    pass


@router.post("/user", tags=["user"])
def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
def forgot_password(request: Request, user: Email = Depends(Email)):
    return BaseController.run(UserController.forgot_password, user.dict(), request)
