from src.controllers import user_bank_accounts
from src.infrastructures.env_config import config
from typing import List

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class BankAccountRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_registered_bank_accounts(cls, unique_id: str):
        data = await cls.find_all(
            query={
                "unique_id": unique_id
            },
            project={
                "_id": 0,
                "bank_accounts": {
                    "$filter": {
                        "input": "$bank_accounts",
                        "as": "item",
                        "cond": {"$eq": ["$$item.status", "active"]}
                    }
                }
            }
        )
        return data[0] if data else data

    @classmethod
    async def save_registered_bank_accounts(cls, unique_id: str, bank_account: dict):
        return await cls.add_one_in_array(
            old={"unique_id": unique_id},
            new={"bank_accounts": bank_account},
            upsert=True
        )

    @classmethod
    async def existing_account_and_is_activated(cls, unique_id: str, bank_account: dict) -> bool:
        data = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "bank": bank_account["bank"],
                        "account_type": bank_account["account_type"],
                        "agency": bank_account["agency"],
                        "account_number": bank_account["account_number"],
                        "status": "active"
                    }
                }
            }
        )
        return bool(data)

    @classmethod
    async def is_bank_account_from_client(cls, unique_id: str, bank_account: dict) -> bool:
        cpf = bank_account['cpf']
        data = await cls.find_one(
            query={
                "unique_id": unique_id,
                "identifier_document.cpf": cpf
            }
        )
        return bool(data)

    @classmethod
    async def bank_account_id_exists(cls, unique_id: str, bank_account_id: str) -> bool:
        data = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "id": bank_account_id
                    }
                }
            }
        )
        return bool(data)

    @classmethod
    async def update_registered_bank_accounts(cls, unique_id: str, bank_account: dict):
        bank_account_id = bank_account['id']
        if 'cpf' in bank_account_id:
            del bank_account_id['cpf']
        was_updated = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts":  {
                    "$elemMatch": {
                        "id": bank_account_id
                    }
                }
            },
            new={
                "bank_accounts.$.bank": bank_account["bank"],
                "bank_accounts.$.account_type": bank_account["account_type"],
                "bank_accounts.$.agency": bank_account["agency"],
                "bank_accounts.$.account_number": bank_account["account_number"],
                "bank_accounts.$.account_name": bank_account["account_name"]
            }
        )
        return was_updated

    @classmethod
    async def delete_registered_bank_accounts(cls, unique_id: str, bank_account: dict):
        bank_account_id = bank_account['id']
        if 'cpf' in bank_account_id:
            del bank_account_id['cpf']
        was_updated = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts":  {
                    "$elemMatch": {
                        "id": bank_account_id
                    }
                }
            },
            new={
                "bank_accounts.$.status": "disabled",
            }
        )
        return was_updated
