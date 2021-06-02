import boto3
from decouple import config
from enum import Enum
import logging

from src.exceptions.exceptions import InternalServerError


class FileType(Enum):
    SELF = 'user_self'


class FileRepository:

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        region_name=config("REGION_NAME"),
    )

    def __init__(self, bucket_name: str):
        self.bucket_name = FileRepository.validate_bucket_name(bucket_name)

    @staticmethod
    def validate_bucket_name(bucket_name: str):
        response = FileRepository.s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in buckets:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(f'The bucket {bucket_name} not exists', exc_info=True)
            raise InternalServerError('files.error')
        return bucket_name

    @staticmethod
    def save_user_file(file_type: FileType, content) -> bool:
        if isinstance(file_type, FileType) is False:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(f'The file type {file_type} not exists', exc_info=True)
            raise InternalServerError('files.error')
        return True
