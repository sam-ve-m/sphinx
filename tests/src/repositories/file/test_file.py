# STANDARD LIBS
import pytest
from unittest.mock import MagicMock, patch
from base64 import b64encode, b64decode
from enum import Enum

# SPHINX
from src.repositories.file.repository import FileRepository, UserFileType, TermsFileType
from src.exceptions.exceptions import InternalServerError, BadRequestError


class S3Client:
    pass


class StubCache:
    pass


@pytest.fixture
@patch.object(FileRepository, "validate_bucket_name", return_value="XXX")
def new_file_repository_valid_mocked_validate_bucket_name(mock_method):
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    S3Client.list_objects = MagicMock(return_value={"Contents": [{"LastModified": "ddd", "Key": "lila"}]})
    S3Client.generate_presigned_url = MagicMock(return_value="link")
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    return FileRepository(bucket_name=name)


@pytest.fixture
@patch.object(FileRepository, "validate_bucket_name", return_value="XXX")
def new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content(
    mock_method,
):
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    S3Client.list_objects = MagicMock(return_value={"Contents": [{"LastModified": "ddd", "Key": "lila"}]})
    S3Client.generate_presigned_url = MagicMock(return_value="link")
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    return FileRepository(bucket_name=name)

@pytest.fixture
@patch.object(FileRepository, "validate_bucket_name", return_value="XXX")
def new_file_repository_valid_mocked_validate_bucket_name_and_s3_without_content(
    mock_method,
):
    name = "XXX"
    S3Client.put_object = MagicMock(return_value={"Buckets": [{"Name": name}]})
    S3Client.list_objects = MagicMock(return_value={"Contents": []})
    S3Client.generate_presigned_url = MagicMock(return_value="link")
    FileRepository.s3_client = S3Client
    FileRepository.validate_bucket_name = MagicMock(return_value=name)
    return FileRepository(bucket_name=name)


def test_init_error() -> None:
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": ""}]})
    FileRepository.s3_client = S3Client
    with pytest.raises(InternalServerError, match="^files.bucket.invalid_name"):
        FileRepository.validate_bucket_name(bucket_name="XXX")


def test_init() -> None:
    name = "XXX"
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    file_repository = FileRepository(bucket_name=name)
    assert file_repository.bucket_name == name

def test_bucket_name_valid() -> None:
    name = "XXX"
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": name}]})
    FileRepository.s3_client = S3Client
    file_repository = FileRepository(bucket_name=name)
    assert file_repository.bucket_name == name

def test_bucket_name_invalid() -> None:
    name = "XXX"
    S3Client.list_buckets = MagicMock(return_value={"Buckets": [{"Name": "mybucket"}]})
    FileRepository.s3_client = S3Client
    with pytest.raises(InternalServerError, match="files.bucket.invalid_name"):
        FileRepository(bucket_name=name)


def test_save_valid_user_file(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    assert (
        file_repository.save_user_file(
            file_type=UserFileType.SELF, content="data", user_email="test@validator"
        )
        is None
    )


def test_save_user_file_with_invalid_user_path(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    file_repository.resolve_user_path = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository.save_user_file(
            file_type=UserFileType.SELF, content="data", user_email="test@validator"
        )


def test_save_user_file_with_invalid_file_extension(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    file_repository.get_file_extension_by_type = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository.save_user_file(
            file_type=UserFileType.SELF, content="data", user_email="test@validator"
        )


def test_resolve_path() -> None:
    path = FileRepository.resolve_user_path(
        user_email="marco@lionx.com.br", file_type=UserFileType.SELF
    )
    assert path == "lionx.com.br/ma/marco@lionx.com.br/user_self/"


def test_resolve_content_byte():
    byte_value = b"1234"
    base64_str = b64encode(byte_value).decode()
    value = FileRepository.resolve_content(content=base64_str)
    assert byte_value == value

def test_resolve_content_str():
    str_value = "1234"
    value = FileRepository.resolve_content(content=str_value)
    base64_bytes = str_value.encode("ascii")
    assert b64decode(base64_bytes) == value

def test_resolve_content_without_value():
    str_value = None
    with pytest.raises(InternalServerError, match="files.content.empty"):
        FileRepository.resolve_content(content=str_value)

def test_save_valid_term_file(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    assert (
        file_repository.save_term_file(
            file_type=TermsFileType.TERM_REFUSAL, content=b"its a byte",
        )
        is None
    )


def test_save_term_file_with_invalid_user_path(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    file_repository.resolve_term_path = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository.save_term_file(file_type=TermsFileType.TERM_REFUSAL, content=b"is a byte")


def test_save_term_file_with_invalid_file_extension(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    file_repository.get_file_extension_by_type = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository.save_term_file(file_type=TermsFileType.TERM_REFUSAL, content=b"is a byte")


def test_get_term_file_none(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    StubCache.get = MagicMock(return_value=None)
    StubCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubCache
    )
    assert value is not None


def test_get_term_file_cache(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    StubCache.get = MagicMock(return_value="lili")
    StubCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubCache
    )
    assert value == "lili"


def test_get_term_file(new_file_repository_valid_mocked_validate_bucket_name) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    S3Client.list_objects = MagicMock(
        return_value={"Contents": [{"LastModified": "ddd", "Key": "lila"}]}
    )
    file_repository.s3_client = S3Client
    StubCache.get = MagicMock(return_value=None)
    StubCache.set = MagicMock(return_value=None)
    value = file_repository.get_term_file(
        file_type=TermsFileType.TERM_REFUSAL, cache=StubCache
    )
    assert value == "link"


def test_get_term_version_file_not_exists(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    file_repository.s3_client.list_objects = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="^files.not_exists"):
        file_repository.get_current_term_version(file_type=TermsFileType.TERM_REFUSAL)


def test_get_term_version(
    new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content,
) -> None:
    file_repository = (
        new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content
    )
    file_repository.s3_client = S3Client
    contents = file_repository.s3_client.list_objects()
    value = file_repository.get_current_term_version(file_type=TermsFileType.TERM_REFUSAL)
    assert value == len(contents.get('Contents'))


def test_get_term_version_is_new_version(
    new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content,
) -> None:
    file_repository = (
        new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content
    )
    file_repository.s3_client = S3Client
    contents = file_repository.s3_client.list_objects()
    value = file_repository.get_current_term_version(file_type=TermsFileType.TERM_REFUSAL)
    new_v = value + 1
    assert new_v > len(contents.get('Contents'))


def test_get_terms_version_without_cache(
    new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content,
) -> None:
    file_repository = (
        new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content
    )
    StubCache.get = MagicMock(return_value=None)
    StubCache.set = MagicMock(return_value=None)
    result = file_repository.get_terms_version(cache=StubCache)
    sum_version = 0
    for key, value in result.items():
        sum_version += value
    assert len(result) == 5
    assert sum_version == 5


def test_get_terms_version_with_cache(
    new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content,
) -> None:
    file_repository = (
        new_file_repository_valid_mocked_validate_bucket_name_and_s3_with_content
    )
    StubCache.get = MagicMock(
        return_value={"la": 1, "le": 1, "li": 1, "lo": 1, "lu": 1}
    )
    result = file_repository.get_terms_version(cache=StubCache)
    sum_version = 0
    for key, value in result.items():
        sum_version += value
    assert len(result) == 5
    assert sum_version == 5


def test_generate_term_file_name_version_none(
    new_file_repository_valid_mocked_validate_bucket_name,
):
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    with pytest.raises(InternalServerError, match="^files.params.invalid"):
        file_repository.generate_term_file_name(name="lala", version=None)


def test_generate_term_file_name_name_none(
    new_file_repository_valid_mocked_validate_bucket_name,
):
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    with pytest.raises(InternalServerError, match="^files.params.invalid"):
        file_repository.generate_term_file_name(name=None, version=1)


def test__get_last_saved_file_from_folder_file_error(
    new_file_repository_valid_mocked_validate_bucket_name,
):
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository._get_last_saved_file_from_folder(path=None)


def test__get_last_saved_file_from_folder_success(
    new_file_repository_valid_mocked_validate_bucket_name,
):
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    assert file_repository._get_last_saved_file_from_folder(path="laalla") is not None


def test_get_file_extension_by_type_valid(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    result = file_repository.get_file_extension_by_type(file_type=UserFileType.SELF)
    assert result == ".jpg"

class FakeEnum(Enum):
    FAKE = "fake"

def test_get_file_extension_by_type_invalid(
    new_file_repository_valid_mocked_validate_bucket_name,
) -> None:
    file_repository = new_file_repository_valid_mocked_validate_bucket_name
    with pytest.raises(InternalServerError, match="^files.error"):
        file_repository.get_file_extension_by_type(FakeEnum.FAKE)


def test_get_terms_version_without_content(
    new_file_repository_valid_mocked_validate_bucket_name_and_s3_without_content,
) -> None:
    file_repository = (
        new_file_repository_valid_mocked_validate_bucket_name_and_s3_without_content
    )
    with pytest.raises(InternalServerError, match="files.error"):
        file_repository._get_last_saved_file_from_folder(path="laalla") is None