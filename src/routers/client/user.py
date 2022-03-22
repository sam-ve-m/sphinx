# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from nidavellir import Sindri

from src.domain.validators.bank_account import CreateBankAccount, UpdateBankAccounts, DeleteBankAccount
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.controllers.user_bank_accounts.controller import UserBankAccounts
from src.routers.routes_registers.client import ClientRouter

router = ClientRouter.instance()


@router.get("/user/bank_accounts", tags=["user"])
async def get_user_bank_accounts(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    return await BaseController.run(UserBankAccounts.get, payload, request)


@router.post("/user/bank_accounts", tags=["user"])
async def create_user_bank_accounts(
        create_bank_account: CreateBankAccount,
        request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": create_bank_account.dict()
    }
    return await BaseController.run(UserBankAccounts.create, payload, request)


@router.put("/user/update_bank_accounts", tags=["user"])
async def update_bank_account(
        update_bank_account: UpdateBankAccounts,
        request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = update_bank_account.dict()
    Sindri.dict_to_primitive_types(obj=bank_account)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account

    }
    return await BaseController.run(UserBankAccounts.update, payload, request)


@router.delete("/user/delete_bank_account", tags=["user"])
async def delete_bank_account(
        delete_bank_account: DeleteBankAccount,
        request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = delete_bank_account.dict()
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account
    }
    return await BaseController.run(UserBankAccounts.delete, payload, request)
