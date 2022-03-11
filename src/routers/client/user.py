# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.controllers.user_bank_accounts.controller import UserBankAccounts
from src.routers.routes_registers.client import ClientRouter

router = ClientRouter.instance()


@router.delete("/user", tags=["user"])
async def delete_user(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    return BaseController.run(UserController.delete, jwt_data, request)


@router.get("/user/bank_accounts", tags=["user"])
async def delete_user(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    return BaseController.run(UserBankAccounts.get, payload, request)


@router.get("/user/bank_accounts", tags=["user"])
async def delete_user( request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    return BaseController.run(UserBankAccounts.get, payload, request)