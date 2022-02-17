# STANDARD LIBS
import pickle
from typing import Optional


# SPHINX
from src.core.interfaces.repositories.redis.interface import IRedis
from src.exceptions.exceptions import InternalServerError
from src.infrastructures.redis.infrastructure import RedisInfrastructure


class RepositoryRedis(RedisInfrastructure, IRedis):
    @staticmethod
    async def set(key: str, value: dict, ttl: int = 0) -> None:
        redis = RepositoryRedis._get_redis()
        """ttl in secounds"""
        if ttl > 0:
            await redis.set(name=key, value=pickle.dumps(value), ex=ttl)
        else:
            await redis.set(name=key, value=pickle.dumps(value))

    @staticmethod
    async def delete(key: str):
        redis = RepositoryRedis._get_redis()
        redis.delete(key)
        return

    @staticmethod
    async def get(key: str) -> Optional[dict]:
        redis = RepositoryRedis._get_redis()
        if type(key) != str:
            raise InternalServerError("cache.error.key")
        value = await redis.get(name=key)
        return value and pickle.loads(value) or value

    @staticmethod
    async def get_keys(pattern: str) -> Optional[list]:
        redis = RepositoryRedis._get_redis()
        return await redis.keys(pattern=pattern)

    @staticmethod
    async def add_to_queue(key: str, value: tuple) -> bool:
        redis = RepositoryRedis._get_redis()
        return await redis.rpush(key, pickle.dumps(value))

    @staticmethod
    async def get_from_queue(key: str) -> Optional[dict]:
        redis = RepositoryRedis._get_redis()
        value = await redis.lpop(name=key)
        return value and pickle.loads(value) or value
