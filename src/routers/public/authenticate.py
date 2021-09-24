from fastapi import Request

from src.controllers.base_controller import BaseController
from src.routers.validators.base import OptionalPIN, Email
from src.controllers.authentications.controller import AuthenticationController
from src.routers.router_registers.public import PublicRouter

router = PublicRouter.instance()


class Login(Email, OptionalPIN):
    pass


@router.post("/login", tags=["authentication"])
def login(user_credentials: Login, request: Request):
    return BaseController.run(AuthenticationController.login, dict(user_credentials), request)
