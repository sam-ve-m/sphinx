# STANDARD LIBS
import logging
from typing import Union, Optional
from base64 import b64decode
from enum import Enum

# OUTSIDE LIBRARIES
import boto3
from decouple import config

# SPHINX
from src.exceptions.exceptions import InternalServerError, BadRequestError
from src.repositories.cache.redis import RepositoryRedis
from src.interfaces.repositories.file_repository.interface import IFile
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.file.enum.user_file import UserFileType


class FileRepository(IFile):

    # This dict keys must be TermsFileType, UserFileType constants
    file_extension_by_type = {
        "user_self": ".jpg",
        "term_application": ".pdf",
        "term_open_account": ".pdf",
        "term_refusal": ".pdf",
        "term_non_compliance": ".pdf",
        "term_retail_liquid_provider": ".pdf",
    }

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        region_name=config("REGION_NAME"),
    )

    def __init__(self, bucket_name: str):
        self.bucket_name = self.validate_bucket_name(bucket_name)

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
        self, file_type: UserFileType, content: Union[str, bytes], user_email: str,
    ) -> None:
        path = self.resolve_user_path(user_email=user_email, file_type=file_type)
        file_name = file_type.value
        file_extension = self.get_file_extension_by_type(file_type=file_type)
        if all([path, file_name, file_extension]) is False:
            raise InternalServerError("files.error")
        self.s3_client.put_object(
            Body=self.resolve_content(content=content),
            Bucket=self.bucket_name,
            Key=f"{path}/{file_name}{file_extension}",
        )

    def save_term_file(
        self, file_type: TermsFileType, content: Union[str, bytes]
    ) -> None:
        if not content or type(content) not in [str, bytes]:
            raise InternalServerError("files.error")
        content = self.resolve_content(content)
        path = self.resolve_term_path(file_type=file_type)
        current_version = self.get_current_term_version(file_type=file_type)
        new_version = current_version + 1
        file_name = self.generate_term_file_name(name=file_type.value, version=new_version)
        file_extension = self.get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key=f"{path}{file_name}{file_extension}",
        )

    def get_term_file(
        self, file_type: TermsFileType, cache=RepositoryRedis, ttl: int = 3600
    ) -> Optional[str]:
        cache_key = f"get_term_file:{file_type.value}"
        cached_value = cache.get(key=cache_key)
        if cached_value:
            return cached_value
        path = self.resolve_term_path(file_type=file_type)
        file_path = self._get_last_saved_file_from_folder(path=path)
        if file_path:
            value = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_path},
                ExpiresIn=ttl,
            )
            cache.set(key=cache_key, value=value, ttl=ttl)
            return value

    def get_terms_version(
        self, term_types=TermsFileType, cache=RepositoryRedis, ttl: int = 3600
    ) -> dict:
        cache_key = "all_terms_version"
        value = cache.get(key=cache_key)
        if value is None:
            value = dict()
            for file_type in term_types:
                value.update(
                    {file_type.value: self.get_current_term_version(file_type=file_type)}
                )
            cache.set(key=cache_key, value=value)
        return value

    def get_term_file_by_version(
        self, file_type: TermsFileType, version: int, ttl: int = 3600
    ) -> str:
        file_name = self.generate_term_file_name(name=file_type.value, version=version)
        path = self.resolve_term_path(file_type=file_type)
        file_extension = self.get_file_extension_by_type(file_type=file_type)
        value = self.s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": f"{path}{file_name}{file_extension}",
            },
            ExpiresIn=ttl,
        )
        return value

    def _get_last_saved_file_from_folder(self, path: str) -> Optional[str]:
        if type(path) is not str:
            raise InternalServerError("files.error")
        objects = self.s3_client.list_objects(
            Bucket=self.bucket_name, Prefix=path, Delimiter="/"
        )
        files_metadata = objects.get("Contents")
        if type(files_metadata) == list and len(files_metadata) > 0:
            sorted(
                files_metadata, key=lambda item: item.get("LastModified"), reverse=True
            )
            return files_metadata[0].get("Key")
        return None

    @staticmethod
    def resolve_content(content: Union[str, bytes]):
        ''' str in this case is a base64 string '''
        if not content:
            raise InternalServerError("files.error")
        if type(content) is str:
            base64_bytes = content.encode("ascii")
            content = b64decode(base64_bytes)
        return content

    @staticmethod
    def resolve_user_path(user_email: str, file_type: UserFileType) -> str:
        name, domain = user_email.split("@")
        return f"{domain}/{name[:2]}/{user_email}/{file_type.value}/"

    @staticmethod
    def get_file_extension_by_type(file_type: Enum) -> Optional[str]:
        valid_files = list()
        for file_enum in [UserFileType, TermsFileType]:
            valid_files += [item.value for item in file_enum]
        if file_type.value not in valid_files:
            raise InternalServerError("files.error")
        return FileRepository.file_extension_by_type.get(file_type.value)

    @staticmethod
    def generate_term_file_name(name: str, version: int):
        if version is None or name is None:
            raise InternalServerError("files.error")
        return f"{name}_v{version}"

    @staticmethod
    def resolve_term_path(file_type: TermsFileType) -> str:
        return f"{file_type.value}/"

    def get_current_term_version(self, file_type: TermsFileType) -> int:
        objects = self.s3_client.list_objects(
            Bucket=self.bucket_name,
            Prefix=FileRepository.resolve_term_path(file_type=file_type),
            Delimiter="/",
        )
        content = objects.get("Contents")
        if type(content) is not list:
            raise BadRequestError("files.not_exists")

        version = len(content)
        return version

