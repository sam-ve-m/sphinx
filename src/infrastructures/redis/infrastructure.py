# OUTSIDE LIBRARIES
from redis import Redis

# SPHINX
from src.utils.env_config import config


class RedisInfrastructure:
    @staticmethod
    def get_redis():
        return Redis(
            host=config("REDIS_HOST"),
            port=config("REDIS_PORT"),
            db=config("REDIS_DB"),
            password=config("REDIS_PASSWORD"),
        )
