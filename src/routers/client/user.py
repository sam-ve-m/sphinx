# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.client import ClientRouter

router = ClientRouter.instance()


@router.delete("/user", tags=["user"])
def delete_user(request: Request):
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)
    return BaseController.run(UserController.delete, jwt_data, request)
