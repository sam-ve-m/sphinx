# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.domain.validators.user_validators import UserSimple

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


@router.post("/user_admin", tags=["user"])
def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)
