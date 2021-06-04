import pytest
from unittest.mock import MagicMock
from base64 import b64encode
from enum import Enum

from src.repositories.file.repository import FileRepository, FileType
from src.exceptions.exceptions import InternalServerError


class S3Client:
    pass


def test_init_error() -> None:
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": ""}]})
    FileRepository.s3_client = S3Client
    with pytest.raises(InternalServerError, match="files.error"):
        FileRepository(bucket_name="XXX")


def test_init() -> None:
    name = "XXX"
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    file_repository = FileRepository(bucket_name=name)
    assert file_repository.bucket_name == name


def test_save_user_file_error() -> None:
    name = "XXX"
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    file_repository = FileRepository(bucket_name=name)
    file_repository.validate_bucket_name = MagicMock(return_value=name)
    with pytest.raises(InternalServerError, match="files.error"):
        file_repository.save_user_file(file_type="", content="", user_email="")


def test_save_user_file() -> None:
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    file_repository.save_user_file(
        file_type=FileType.SELF, content="", user_email="test@validator"
    )
    assert True


def test_resolve_path() -> None:
    path = FileRepository.resolve_user_path(
        user_email="marco@lionx.com.br", file_type=FileType.SELF
    )
    assert path == "lionx.com.br/ma/marco@lionx.com.br/user_self/"


def test_resolve_content_str():
    str_value = b"1234"
    base64_str = b64encode(str_value).decode()
    value = FileRepository.resolve_content(content=base64_str)
    assert str_value == value


def test_save_term_file_v1() -> None:
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    S3Client.list_objects = MagicMock(return_value={})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    file_repository.save_term_file(
        file_type=FileType.TERM_REFUSAL, content="",
    )
    assert True


class StubbyFileType(Enum):
    TEST = 'test'


class StubbyCache(Enum):
    pass


def test_get_term_file_none() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={})
    S3Client.generate_presigned_url = MagicMock(return_value='link')
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value=None)
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(file_type=StubbyFileType.TEST, cache=StubbyCache)
    assert value is None


def test_get_term_file_cache() -> None:
    name = "dtvm-test"
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value='lili')
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(file_type=StubbyFileType.TEST, cache=StubbyCache)
    assert value == 'lili'


def test_get_term_file() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={"Contents": [{"LastModified": name, "Key": 'lila'}]})
    S3Client.generate_presigned_url = MagicMock(return_value='link')
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value=None)
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(file_type=StubbyFileType.TEST, cache=StubbyCache)
    assert value == 'link'