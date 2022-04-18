from src.infrastructures.env_config import config
from src.exceptions.exceptions import InternalServerError

from etria_logger import Gladsheim
from src.infrastructures.s3.infrastructure import S3Infrastructure
from src.repositories.cache.repository import RepositoryRedis

JWT_FILE_BUCKET_NAME = config("JWT_FILE_BUCKET_NAME")


class Bucket:

    infra = S3Infrastructure
    cache = RepositoryRedis

    @classmethod
    async def get_jwt_key_file(cls, bucket_name: str) -> str:
        found_key = await cls.cache.get(key=JWT_FILE_BUCKET_NAME)
        if not found_key:
            try:
                async with cls.infra.get_bucket(bucket_name) as bucket:
                    body = None
                    async for obj in bucket.objects.all():
                        key = obj.key
                        if key == f"{JWT_FILE_BUCKET_NAME}.json":
                            body = await obj.get()

                    if body is None:
                        raise InternalServerError("Error on get secrets")

                    value = await body["Body"].read()
                    await cls.cache.set(key=JWT_FILE_BUCKET_NAME, value=value)

                    return value
            except Exception as e:
                Gladsheim.error(error=e)

        return found_key.decode()
