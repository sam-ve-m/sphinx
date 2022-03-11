# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.repositories.bank_account.repository import BankAccountRepository


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]


    @classmethod
    async def update_user_bank_accounts(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        old = await bank_account_repository.find_one()

    @classmethod
    async def delete_user_bank_accounts(
                cls, payload: dict, bank_account_repository=BankAccountRepository
        ):
            thebes_answer = payload.get("x-thebes-answer")
            unique_id = thebes_answer["user"]["unique_id"]

            return {
                "status_code": status.HTTP_200_OK,
                "payload": {"bank_accounts": bank_accounts},
            }
    @classmethod
    async def get_user_bank_accounts(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        bank_accounts = await bank_account_repository.get_registered_bank_accounts(
            unique_id=unique_id
        )
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"bank_accounts": bank_accounts},
        }








