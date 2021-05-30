from decouple import config
from redis import Redis
from typing import Optional
from datetime import datetime
import pickle


class RepositoryRedis:

    # Behind the scenes, redis-py uses a connection pool to manage connections to a Redis server.
    # https://pypi.org/project/redis/#connection-pools
    redis = (
            eval(config("PRODUCTION")) is True
            and Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=config('REDIS_DB'), password=config('REDIS_PASSWORD'))
            or Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=config('REDIS_DB'))
    )

    @staticmethod
    def set(key: str, value: dict, redis=redis, ttl:int = 0):
        '''ttl in secounds'''
        if ttl > 0:
            redis.set(name=key, value=pickle.dumps(value), ex=ttl)
        else:
            redis.set(name=key, value=pickle.dumps(value))

    @staticmethod
    def get(key: str, redis=redis) -> Optional[dict]:
        value = redis.get(name=key)
        return value and pickle.loads(value) or value

    @staticmethod
    def get_keys(pattern: str, redis=redis) -> Optional[list]:
        return redis.keys(pattern=pattern)

    @staticmethod
    def add_to_queue(key: str, value: tuple, redis=redis):
        return redis.rpush(key, pickle.dumps(value))

    @staticmethod
    def get_from_queue(key: str, redis=redis):
        value = redis.lpop(name=key)
        return value and pickle.loads(value) or value
