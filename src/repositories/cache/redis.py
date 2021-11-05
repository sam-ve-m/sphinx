# STANDARD LIBS
import pickle
from typing import Optional


# SPHINX
from src.core.interfaces.repositories.redis.interface import IRedis
from src.exceptions.exceptions import InternalServerError
from src.infrastructures.redis.infrastructure import RedisInfrastructure


class RepositoryRedis(RedisInfrastructure, IRedis):

    @staticmethod
    def set(key: str, value: dict, ttl: int = 0) -> None:
        redis = RepositoryRedis._get_redis()
        """ttl in secounds"""
        if ttl > 0:
            redis.set(name=key, value=pickle.dumps(value), ex=ttl)
        else:
            redis.set(name=key, value=pickle.dumps(value))

    @staticmethod
    def delete(key: str):
        redis = RepositoryRedis._get_redis()
        redis.delete(key)
        return

    @staticmethod
    def get(key: str) -> Optional[dict]:
        redis = RepositoryRedis._get_redis()
        if type(key) != str:
            raise InternalServerError("cache.error.key")
        value = redis.get(name=key)
        return value and pickle.loads(value) or value

    @staticmethod
    def get_keys(pattern: str) -> Optional[list]:
        redis = RepositoryRedis._get_redis()
        return redis.keys(pattern=pattern)

    @staticmethod
    def add_to_queue(key: str, value: tuple) -> bool:
        redis = RepositoryRedis._get_redis()
        return redis.rpush(key, pickle.dumps(value))

    @staticmethod
    def get_from_queue(key: str) -> Optional[dict]:
        redis = RepositoryRedis._get_redis()
        value = redis.lpop(name=key)
        return value and pickle.loads(value) or value
