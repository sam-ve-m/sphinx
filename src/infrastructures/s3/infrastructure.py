# OUTSIDE LIBRARIES
import aioboto3
import logging
from contextlib import asynccontextmanager

# Sphinx
from src.infrastructures.env_config import config
from src.exceptions.exceptions import InternalServerError


class S3Infrastructure:

    session = None

    @classmethod
    async def _get_session(cls):
        if cls.session is None:
            cls.session = aioboto3.Session(
                aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                region_name=config("REGION_NAME")
            )
        return cls.session

    @classmethod
    @asynccontextmanager
    async def _get_client(cls, bucket_name):
        session = await S3Infrastructure._get_session()
        async with session.client("s3") as s3_client:
            yield s3_client

    @classmethod
    @asynccontextmanager
    async def _get_resource(cls, bucket_name):
        session = await S3Infrastructure._get_session()
        async with session.resource("s3") as s3_resource:
            yield s3_resource
