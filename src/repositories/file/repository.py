# STANDARD LIBS
from io import BytesIO
from typing import Union, Optional
from base64 import b64decode
from enum import Enum

# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.exceptions.exceptions import InternalServerError, BadRequestError
from src.infrastructures.s3.infrastructure import S3Infrastructure
from src.repositories.cache.redis import RepositoryRedis
from src.core.interfaces.repositories.file_repository.interface import IFile
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.file.enum.user_file import UserFileType


class FileRepository(S3Infrastructure, IFile):

    # This dict keys must be TermsFileType, UserFileType constants
    file_extension_by_type = {
        "user_selfie": ".jpg",
        "term_application": ".pdf",
        "term_open_account": ".pdf",
        "term_refusal": ".pdf",
        "term_non_compliance": ".pdf",
        "term_retail_liquid_provider": ".pdf",
    }

    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name

    async def save_user_file(
        self,
        file_type: UserFileType,
        content: Union[str, bytes],
        unique_id: str,
    ) -> str:
        path = await self.resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = await self.get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        async with FileRepository._get_client(self.bucket_name) as s3_client:
            await s3_client.upload_fileobj(
                self.resolve_content(content=content),
                self.bucket_name,
                fully_qualified_path,
            )
        return fully_qualified_path

    async def get_user_selfie(
        self,
        file_type: UserFileType,
        unique_id: str,
    ) -> Union[str, dict]:
        path = await self.resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = await self.get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        s3_client = await FileRepository._get_client(self.bucket_name)
        value = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": fully_qualified_path},
            ExpiresIn=604800,
        )
        # week link validation
        return value

    async def user_file_exists(self, file_type: UserFileType, unique_id: str):
        prefix = await self.resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = await self.get_file_extension_by_type(file_type=file_type)
        if not prefix or not file_name or not file_extension:
            raise InternalServerError("files.error")

        objects = None
        async with FileRepository._get_resource(self.bucket_name) as s3_resource:
            bucket = await s3_resource.Bucket(self.bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=prefix):
                objects = s3_object

        if not objects:
            exists_selfie = False
        else:
            exists_selfie = True

        return exists_selfie

    async def save_term_file(
        self, file_type: TermsFileType, content: Union[str, bytes]
    ) -> None:
        path = self.resolve_term_path(file_type=file_type)
        current_version = await self.get_current_term_version(file_type=file_type)
        new_version = current_version + 1
        file_name = self.generate_term_file_name(
            name=file_type.value, version=new_version
        )
        file_extension = await self.get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        async with FileRepository._get_client(self.bucket_name) as s3_client:
            await s3_client.upload_fileobj(
                self.resolve_content(content),
                self.bucket_name,
                f"{path}{file_name}{file_extension}"
            )
        return

    async def get_term_file(
        self, file_type: TermsFileType, cache=RepositoryRedis, ttl: int = 3600
    ) -> Union[str, dict]:
        cache_key = f"get_term_file:{file_type.value}"
        cached_value = await cache.get(key=cache_key)
        if cached_value:
            return cached_value
        path = self.resolve_term_path(file_type=file_type)
        try:
            file_path = self._get_last_saved_file_from_folder(path=path)
        except InternalServerError:
            return
        else:
            if not file_path:
                return
            async with FileRepository._get_client(self.bucket_name) as s3_client:
                value = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": file_path},
                    ExpiresIn=ttl,
                )
            await cache.set(key=cache_key, value=value, ttl=ttl)
            return value

    async def get_terms_version(
        self, term_types=TermsFileType, cache=RepositoryRedis, ttl: int = 3600
    ) -> dict:
        value = dict()
        for file_type in term_types:
            value.update(
                {
                    file_type.value: await self.get_current_term_version(
                        file_type=file_type
                    )
                }
            )
        return value

    async def get_term_file_by_version(
        self, file_type: TermsFileType, version: int, ttl: int = 3600
    ) -> str:
        file_name = await self.generate_term_file_name(name=file_type.value, version=version)
        path = self.resolve_term_path(file_type=file_type)
        file_extension = await self.get_file_extension_by_type(file_type=file_type)
        async with FileRepository._get_client(self.bucket_name) as s3_client:
            value = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": f"{path}{file_name}{file_extension}",
                },
                ExpiresIn=ttl,
            )
        return value

    async def _get_last_saved_file_from_folder(self, path: str) -> Optional[str]:
        if type(path) is not str:
            raise InternalServerError("files.error")

        objects = {}
        async with FileRepository._get_resource(self.bucket_name) as s3_resource:
            bucket = await s3_resource.Bucket(self.bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=path, Delimiter="/"):
                objects = s3_object

        files_metadata = objects.get("Contents")
        if files_metadata is None:
            raise InternalServerError("files.is_none")
        if not type(files_metadata) == list:
            raise InternalServerError("files.is_not_list")
        if not len(files_metadata) > 0:
            raise InternalServerError("files.is_empty")

        files_metadata = sorted(
            files_metadata, key=lambda item: item.get("LastModified"), reverse=True
        )
        return files_metadata[0].get("Key")

    @staticmethod
    def resolve_content(content: Union[str, bytes]) -> BytesIO:
        """str in this case is a base64 string"""
        if content is None:
            raise InternalServerError("files.content.empty")
        if type(content) is str:
            base64_bytes = content.encode("ascii")
            content = b64decode(base64_bytes)
        bytes_io = BytesIO()
        bytes_io.write(content)
        bytes_io.seek(0)
        return bytes_io

    @staticmethod
    async def resolve_user_path(unique_id: str, file_type: UserFileType) -> str:
        return f"{unique_id}/{file_type.value}/"

    @staticmethod
    async def get_file_extension_by_type(file_type: Enum) -> Optional[str]:
        valid_files = list()
        for file_enum in [UserFileType, TermsFileType]:
            valid_files += [item.value for item in file_enum]
        if file_type.value not in valid_files:
            raise InternalServerError("files.error")
        return FileRepository.file_extension_by_type.get(file_type.value)

    @staticmethod
    async def generate_term_file_name(name: str, version: int):
        if version is None or name is None:
            raise InternalServerError("files.params.invalid")
        return f"{name}_v{version}"

    @staticmethod
    def resolve_term_path(file_type: TermsFileType) -> str:
        return f"{file_type.value}/"

    async def get_current_term_version(self, file_type: TermsFileType) -> int:
        async with FileRepository._get_resource(self.bucket_name) as s3_resource:
            bucket = await s3_resource.Bucket(self.bucket_name)
            prefix = FileRepository.resolve_term_path(file_type=file_type)
            version = 0
            async for s3_object in bucket.objects.filter(Prefix=prefix, Delimiter="/"):
                version += 1
        if not version:
            raise BadRequestError("files.not_exists")
        return version
