# OUTSIDE LIBRARIES
from fastapi import Depends, Request

# SPHINX
from src.domain.validators.user_validators import UserSimple
from src.domain.validators.base import Email
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.public import PublicRouter

router = PublicRouter.instance()


@router.post("/user", tags=["user"])
async def create_user(user: UserSimple, request: Request):
    return await BaseController.run(UserController.create, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
async def forgot_password(request: Request, user: Email = Depends(Email)):
    return await BaseController.run(UserController.forgot_password, user.dict(), request)
