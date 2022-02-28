# OUTSIDE LIBRARIES
from fastapi import Request

from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

# SPHINX
from src.domain.validators.user_validators import UserSimple
from src.routers.routes_registers.public import PublicRouter

router = PublicRouter.instance()


@router.post("/user", tags=["user"])
async def create_user(user: UserSimple, request: Request):
    return await BaseController.run(UserController.create, dict(user), request)
