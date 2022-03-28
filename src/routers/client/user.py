# OUTSIDE LIBRARIES
from fastapi import Request
# SPHINX
from nidavellir import Sindri

from src.controllers.base_controller import BaseController
from src.controllers.user_bank_accounts.controller import UserBankAccounts
from src.domain.validators.bank_account import CreateUserBankAccount, UpdateUserBankAccounts, DeleteUsersBankAccount
from src.routers.routes_registers.client import ClientRouter
from src.services.jwts.service import JwtService

router = ClientRouter.instance()


@router.get("/user/bank_accounts", tags=["user"])
async def get_user_bank_accounts(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    get_user_bank_accounts_response = await BaseController.run(UserBankAccounts.get, payload, request)
    return get_user_bank_accounts_response


@router.post("/user/bank_accounts", tags=["user"])
async def create_user_bank_accounts(
        create_bank_account: CreateUserBankAccount,
        request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": create_bank_account.dict()
    }
    create_user_bank_accounts_response = await BaseController.run(UserBankAccounts.create, payload, request)
    return create_user_bank_accounts_response


@router.put("/user/bank_accounts", tags=["user"])
async def update_bank_account(
        update_bank_account: UpdateUserBankAccounts,
        request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = update_bank_account.dict()
    Sindri.dict_to_primitive_types(obj=bank_account)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account

    }
    update_bank_account_response = await BaseController.run(UserBankAccounts.update, payload, request)
    return update_bank_account_response


@router.delete("/user/bank_account", tags=["user"])
async def delete_bank_account(
        delete_bank_account: DeleteUsersBankAccount,
        request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = delete_bank_account.dict()
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account
    }
    delete_bank_account_response = await BaseController.run(UserBankAccounts.delete, payload, request)
    return delete_bank_account_response
