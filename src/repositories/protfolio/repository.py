from src.repositories.base_repository.redis.base import BaseRepositoryRedis
from src.infrastructures.env_config import config


class PortfolioRepository(BaseRepositoryRedis):
    redis_host = config("REDIS_HOST_URL")
    redis_db = config("REDIS_PORTFOLIO_DB")
    prefix = ""

    @classmethod
    async def save_unique_id_by_account(cls, account: str, unique_id: str, region: str):
        key = f"symbolic_user_id:{region}:{account}"
        await cls.set_without_pickle(key, unique_id)
