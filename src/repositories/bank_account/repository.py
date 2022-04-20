from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.infrastructures.env_config import config

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class UserBankAccountRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_registered_user_bank_accounts(cls, unique_id: str) -> list:
        response = None
        user_bank_accounts_by_unique_id = await cls.find_all(
            query={"unique_id": unique_id},
            project={
                "_id": 0,
                "bank_accounts": {
                    "$filter": {
                        "input": "$bank_accounts",
                        "as": "item",
                        "cond": {"$eq": ["$$item.status", "active"]},
                    }
                },
            },
        )

        has_user_bank_accounts_by_unique_id = (
            user_bank_accounts_by_unique_id is not None
        )
        if has_user_bank_accounts_by_unique_id:
            response = user_bank_accounts_by_unique_id[0]

        return response

    @classmethod
    async def save_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ) -> bool:
        user_bank_account_was_added = await cls.add_one_in_array(
            old={"unique_id": unique_id},
            new={"bank_accounts": bank_account},
            upsert=True,
        )
        return user_bank_account_was_added

    @classmethod
    async def existing_user_bank_account_and_is_activated(
        cls, unique_id: str, bank_account: dict
    ) -> bool:
        user_bank_account = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "bank": bank_account["bank"],
                        "account_type": bank_account["account_type"],
                        "agency": bank_account["agency"],
                        "account_number": bank_account["account_number"],
                        "status": UserBankAccountStatus.ACTIVE.value,
                    }
                },
            }
        )
        has_user_bank_account = bool(user_bank_account)
        return has_user_bank_account

    @classmethod
    async def is_user_bank_account_from_client(
        cls, unique_id: str, bank_account: dict
    ) -> bool:
        cpf = bank_account["cpf"]
        user_bank_account = await cls.find_one(
            query={"unique_id": unique_id, "identifier_document.cpf": cpf}
        )
        is_user_bank_account_from_client = bool(user_bank_account)
        return is_user_bank_account_from_client

    @classmethod
    async def user_bank_account_id_exists(
        cls, unique_id: str, bank_account_id: str
    ) -> bool:
        user_bank_account = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            }
        )
        user_bank_account_id_exists = bool(user_bank_account)
        return user_bank_account_id_exists

    @classmethod
    async def update_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ):
        bank_account_id = bank_account["id"]
        if "cpf" in bank_account_id:
            del bank_account_id["cpf"]

        user_bank_account_was_updated = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            },
            new={
                "bank_accounts.$.bank": bank_account["bank"],
                "bank_accounts.$.account_type": bank_account["account_type"],
                "bank_accounts.$.agency": bank_account["agency"],
                "bank_accounts.$.account_number": bank_account["account_number"],
                "bank_accounts.$.account_name": bank_account["account_name"],
            },
        )
        return user_bank_account_was_updated

    @classmethod
    async def delete_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ):
        bank_account_id = bank_account["id"]
        if "cpf" in bank_account_id:
            del bank_account_id["cpf"]
        user_bank_account_was_soft_deleted = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            },
            new={
                "bank_accounts.$.status": UserBankAccountStatus.DISABLED.value,
            },
        )
        return user_bank_account_was_soft_deleted
