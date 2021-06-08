# STANDARD LIBS
import pytest
from unittest.mock import MagicMock
from base64 import b64encode
from enum import Enum

# SPHINX
from src.repositories.file.repository import FileRepository, UserFileType, TermsFileType
from src.exceptions.exceptions import InternalServerError, BadRequestError


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


def test_save_user_file() -> None:
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    file_repository.save_user_file(
        file_type=UserFileType.SELF, content="", user_email="test@validator"
    )
    assert True


def test_resolve_path() -> None:
    path = FileRepository.resolve_user_path(
        user_email="marco@lionx.com.br", file_type=UserFileType.SELF
    )
    assert path == "lionx.com.br/ma/marco@lionx.com.br/user_self/"


def test_resolve_content_str():
    str_value = b"1234"
    base64_str = b64encode(str_value).decode()
    value = FileRepository.resolve_content(content=base64_str)
    assert str_value == value


def test_save_term_file() -> None:
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    S3Client.list_objects = MagicMock(return_value={})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    file_repository.save_term_file(
        file_type=TermsFileType.TERM_REFUSAL, content="",
    )
    assert True


class StubbyCache:
    pass


def test_get_term_file_none() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={})
    S3Client.generate_presigned_url = MagicMock(return_value="link")
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value=None)
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubbyCache
    )
    assert value is None


def test_get_term_file_cache() -> None:
    name = "dtvm-test"
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value="lili")
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubbyCache
    )
    assert value == "lili"


def test_get_term_file() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(
        return_value={"Contents": [{"LastModified": name, "Key": "lila"}]}
    )
    S3Client.generate_presigned_url = MagicMock(return_value="link")
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value=None)
    StubbyCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubbyCache
    )
    assert value == "link"


def test_get_term_version_file_not_exists() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={"Contents": []})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    with pytest.raises(BadRequestError, match="files.not_exists"):
        file_repository.get_term_version(file_type=TermsFileType.TERM_REFUSAL)


def test_get_term_version() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={"Contents": [1, 2, 3]})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)

    value = file_repository.get_term_version(file_type=TermsFileType.TERM_REFUSAL)
    assert value == 3


def test_get_term_version_is_new_version() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={"Contents": [1, 2, 3]})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)

    value = file_repository.get_term_version(
        file_type=TermsFileType.TERM_REFUSAL, is_new_version=True
    )
    assert value == 4


def test_get_terms_version_without_cache() -> None:
    name = "dtvm-test"
    S3Client.list_objects = MagicMock(return_value={"Contents": [1, 2, 3]})
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(return_value=None)
    StubbyCache.set = MagicMock(return_value=None)
    result = file_repository.get_terms_version(cache=StubbyCache)
    sum_version = 0
    for key, value in result.items():
        sum_version += value
    assert len(result) == 5
    assert sum_version == 15


def test_get_terms_version_with_cache() -> None:
    name = "dtvm-test"
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    file_repository = FileRepository(bucket_name=name)
    StubbyCache.get = MagicMock(
        return_value={"la": 1, "le": 1, "li": 1, "lo": 1, "lu": 1}
    )
    result = file_repository.get_terms_version(cache=StubbyCache)
    sum_version = 0
    for key, value in result.items():
        sum_version += value
    assert len(result) == 5
    assert sum_version == 5
