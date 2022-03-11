from src.infrastructures.env_config import config
# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class BankAccountRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_registered_bank_accounts(cls, unique_id: str):
        data = await cls.find_one(query={}, project={"unique_id": 1, "bank_accounts": 1})
        return data

    @classmethod
    async def existing_account(cls, unique_id: str, bank_account: dict) -> bool:
        data = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "bank": bank_account["bank"],
                        "account_type": bank_account["account_type"],
                        "agency": bank_account["agency"],
                        "account_number": bank_account["account_number"]
                    }
                }
            },
            project={"unique_id": 1}
        )
        return bool(data)
