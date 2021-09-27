# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.routers.validators.base import (
    Email,
    OptionalPIN,
    NickName,
)

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


# TODO: remove validatro from herer
class UserSimple(Email, NickName, OptionalPIN):
    pass


@router.post("/user_admin", tags=["user"])
def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)
