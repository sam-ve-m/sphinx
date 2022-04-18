from src.repositories.base_repository.redis.base import BaseRepositoryRedis
from src.infrastructures.env_config import config


class RepositoryRedis(BaseRepositoryRedis):
   redis_host = config("REDIS_HOST_URL")
   redis_db = config("REDIS_CACHE_DB")
   prefix = "sphinx:"