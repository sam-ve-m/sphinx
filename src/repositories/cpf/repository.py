# OUTSIDE LIBRARIES

from src.infrastructures.env_config import config

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class AllowedCpf(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_ALLOWED_CPF")

    @classmethod
    async def is_cpf_allowed(cls, cpf: str):
        is_allowed = await cls.find_one({"cpf": cpf})
        return bool(is_allowed)
