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
