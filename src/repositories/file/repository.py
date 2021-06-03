import boto3
from decouple import config
from enum import Enum
import logging
from typing import Union, Optional
from base64 import b64decode

from src.exceptions.exceptions import InternalServerError


class FileType(Enum):
    SELF = "user_self"
    TERM = "term"


class FileRepository:

    # This dict keys must be FileType constants
    file_extension_by_type = {"user_self": ".jpg", "term": ".pdf"}

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
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        if bucket_name not in buckets:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(f"The bucket {bucket_name} not exists", exc_info=True)
            raise InternalServerError("files.error")
        return bucket_name

    def save_user_file(
        self, file_type: FileType, content: Union[str, bytes], user_email: str,
    ) -> None:
        if isinstance(file_type, FileType) is False:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(f"The file type {file_type} not exists", exc_info=True)
            raise InternalServerError("files.error")
        path = FileRepository.resolve_user_path(
            user_email=user_email, file_type=file_type
        )
        file_name = file_type.value
        file_extension = FileRepository.get_file_extension_by_type(file_type=file_type)
        self.s3_client.put_object(
            Body=FileRepository.resolve_content(content=content),
            Bucket=self.bucket_name,
            Key=f"{path}/{file_name}{file_extension}",
        )

    def save_term_file(
        self, file_type: FileType, content: Union[str, bytes]
    ) -> None:
        if isinstance(file_type, FileType) is False:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(f"The file type {file_type} not exists", exc_info=True)
            raise InternalServerError("files.error")
        path = FileRepository.resolve_term_path(file_type=file_type)
        file_name = self._get_term_name(file_type=file_type, path=path)
        file_extension = FileRepository.get_file_extension_by_type(file_type=file_type)
        self.s3_client.put_object(
            Body=FileRepository.resolve_content(content=content),
            Bucket=self.bucket_name,
            Key=f"{path}{file_name}{file_extension}",
        )

    @staticmethod
    def resolve_content(content: Union[str, bytes]):
        if type(content) == str:
            base64_bytes = content.encode("ascii")
            content = b64decode(base64_bytes)
        return content

    @staticmethod
    def resolve_user_path(user_email: str, file_type: FileType) -> str:
        name, domain = user_email.split("@")
        return f"{domain}/{name[:2]}/{user_email}/{file_type.value}/"

    @staticmethod
    def resolve_term_path(file_type: FileType) -> str:
        return f"{file_type.value}/"

    @staticmethod
    def get_file_extension_by_type(file_type: FileType) -> Optional[str]:
        return FileRepository.file_extension_by_type.get(file_type.value)

    def _get_term_name(self, file_type: FileType, path: str) -> str:
        base_name = file_type.value
        objects = self.s3_client.list_objects(
            Bucket=self.bucket_name,
            Prefix=path,
            Delimiter='/'
        )
        content = objects.get('Contents')
        version = 1
        if content:
            version = len(content) + 1
        return f'{base_name}_v{version}'
