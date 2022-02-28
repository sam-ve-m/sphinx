# OUTSIDE LIBRARIES
import aioredis

# SPHINX
from src.infrastructures.env_config import config


class RedisInfrastructure:
    redis = None

    @classmethod
    def get_redis(cls):
        if cls.redis is None:
            url = config("REDIS_HOST_URL")
            cls.redis = aioredis.from_url(url)
        return cls.redis
