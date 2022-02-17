# OUTSIDE LIBRARIES
from redis import Redis

# SPHINX
from src.infrastructures.env_config import config


class RedisInfrastructure:

    redis = None

    @classmethod
    def _get_redis(cls):
        if cls.redis is None:
            cls.redis = Redis(
                host=config("REDIS_HOST"),
                port=config("REDIS_PORT"),
                db=config("REDIS_DB"),
                username=config("REDIS_USER"),
                password=config("REDIS_PASSWORD"),
            )
        return cls.redis
