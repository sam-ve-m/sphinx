# STANDARD LIBS
from uuid import uuid4

# OUTSIDE LIBRARIES
import activity as activity
from fastapi import status
from src.exceptions.exceptions import InternalServerError

# SPHINX
from src.repositories.bank_account.repository import BankAccountRepository
from src.exceptions.exceptions import BadRequestError


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]

        is_bank_account_from_user = (
            await bank_account_repository.is_bank_account_from_client(unique_id=unique_id, bank_account=bank_account)
        )
        if not is_bank_account_from_user:
            raise BadRequestError("user.bank_account_is_not_yours")

        bank_account_exists_and_is_activated = (
            await bank_account_repository.existing_account_and_is_activated(unique_id=unique_id, bank_account=bank_account)
        )
        if bank_account_exists_and_is_activated:
            raise BadRequestError("common.register_exists")

        bank_account.update({
            "id": uuid4(),
            "status": "active"
        })
        if "cpf" in bank_account:
            del bank_account['cpf']

        if not await BankAccountRepository.save_registered_bank_accounts(
                unique_id=unique_id,
                bank_account=bank_account
        ):
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.created",
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
        if bank_accounts is None:
            bank_accounts = {"bank_accounts": []}
        return {
            "status_code": status.HTTP_200_OK,
            "payload": bank_accounts,
        }

    @classmethod
    async def update_bank_account(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]
        bank_account_id = bank_account["id"]
        bank_account_exists = (
            await bank_account_repository.bank_account_id_exists(unique_id=unique_id, bank_account_id=bank_account_id)
        )
        if not bank_account_exists:
            raise BadRequestError("common.register_not_exists")

        was_updated = (
            await bank_account_repository.update_registered_bank_accounts(unique_id=unique_id, bank_account=bank_account)
        )
        if not was_updated:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @classmethod
    async def delete_bank_account(
            cls, payload: dict, bank_account_repository=BankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]
        bank_account_id = bank_account["id"]
        bank_account_exists = (
            await bank_account_repository.bank_account_id_exists(unique_id=unique_id, bank_account_id=bank_account_id)
        )
        if not bank_account_exists:
            raise BadRequestError("common.register_not_exists")

        was_deleted = (
            await bank_account_repository.delete_registered_bank_accounts(unique_id=unique_id, bank_account=bank_account)
        )
        if not was_deleted:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.deleted",
        }

