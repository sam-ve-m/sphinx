# OUTSIDE LIBRARIES
import aioredis

# SPHINX
from src.infrastructures.env_config import config


class RedisInfrastructure:
    redis = None

    @classmethod
    def _get_redis(cls):
        if cls.redis is None:
            url = "redis://{}:{}@{}:{}?db={}".format(
                config("KEY_REDIS_USER"),
                config("KEY_REDIS_PASSWORD"),
                config("KEY_REDIS_HOST"),
                config("KEY_REDIS_PORT"),
                config("KEY_REDIS_DB")
            )
            cls.redis = aioredis.from_url(url)

        return cls.redis

