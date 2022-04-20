# STANDARD LIBS
from uuid import uuid4

# OUTSIDE LIBRARIES
from fastapi import status

from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.exceptions.exceptions import BadRequestError
from src.exceptions.exceptions import InternalServerError

# SPHINX
from src.repositories.bank_account.repository import UserBankAccountRepository


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
        cls, payload: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]

        is_bank_account_from_user = (
            await bank_account_repository.is_user_bank_account_from_client(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not is_bank_account_from_user:
            raise BadRequestError("user.bank_account_is_not_yours")

        bank_account_exists_and_is_activated = (
            await bank_account_repository.existing_user_bank_account_and_is_activated(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if bank_account_exists_and_is_activated:
            raise BadRequestError("common.register_exists")

        bank_account.update(
            {"id": uuid4(), "status": UserBankAccountStatus.ACTIVE.value}
        )
        if "cpf" in bank_account:
            del bank_account["cpf"]

        user_bank_account_was_added = (
            await UserBankAccountRepository.save_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )

        if not user_bank_account_was_added:
            raise InternalServerError("common.process_issue")

        create_account_response = {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.created",
        }

        return create_account_response

    @classmethod
    async def get_user_bank_accounts(
        cls, payload: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        bank_accounts = await bank_account_repository.get_registered_user_bank_accounts(
            unique_id=unique_id
        )
        if bank_accounts is None:
            bank_accounts = {"bank_accounts": []}

        get_user_bank_accounts_response = {
            "status_code": status.HTTP_200_OK,
            "payload": bank_accounts,
        }

        return get_user_bank_accounts_response

    @classmethod
    async def update_user_bank_account(
        cls, payload: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]
        bank_account_id = bank_account["id"]
        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account_id
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        user_bank_account_was_updated = (
            await bank_account_repository.update_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not user_bank_account_was_updated:
            raise InternalServerError("common.process_issue")

        update_bank_account_response = {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

        return update_bank_account_response

    @classmethod
    async def delete_user_bank_account(
        cls, payload: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = payload["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = payload["bank_account"]
        bank_account_id = bank_account["id"]
        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account_id
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        user_bank_account_was_soft_deleted = (
            await bank_account_repository.delete_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not user_bank_account_was_soft_deleted:
            raise InternalServerError("common.process_issue")

        delete_bank_account_response = {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.deleted",
        }

        return delete_bank_account_response
