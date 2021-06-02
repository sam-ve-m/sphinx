import pytest
from unittest.mock import MagicMock

from src.repositories.file.file import FileRepository, FileType
from src.exceptions.exceptions import InternalServerError


class S3Client:
    pass


def test_init_error() -> None:
    S3Client.list_buckets = MagicMock(return_value={'Buckets': [{'Name': ''}]})
    FileRepository.s3_client = S3Client
    with pytest.raises(InternalServerError, match='files.error'):
        FileRepository(bucket_name='XXX')


def test_init() -> None:
    name = 'XXX'
    S3Client.list_buckets = MagicMock(return_value={'Buckets': [{'Name': name}]})
    FileRepository.s3_client = S3Client
    file_repository = FileRepository(bucket_name=name)
    assert file_repository.bucket_name == name


def test_save_user_file_error() -> None:
    with pytest.raises(InternalServerError, match='files.error'):
        FileRepository.save_user_file(file_type='XXX', content='')
