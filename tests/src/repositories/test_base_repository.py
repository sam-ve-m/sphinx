# STANDARD LIBS
from enum import Enum

# OUTSIDE LIBRARIES
from decouple import config
from unittest.mock import MagicMock

# SPHINX
from tests.stub_classes.stub_base_repository import StubBaseRepository
from src.repositories.base_repository import BaseRepository


class StubUser(StubBaseRepository):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_USER_COLLECTION"),
        )


def test_insert_user() -> None:
    stub_user = StubUser()
    stub_user.insert = MagicMock(return_value=True)
    done = stub_user.insert({"name": "stub Guy"})
    assert done is True


def test_insert_many_users() -> None:
    stub_user = StubUser()
    stub_user.insert_many = MagicMock(return_value=True)
    done = stub_user.insert_many([{"name": "stub Guy 3"}, {"name": "stub Guy 3"}])
    assert done is True


def test_find_many_users() -> None:
    stub_user = StubUser()
    done = stub_user.find_all()
    assert done is list


def test_find_more_then_one_equal_user() -> None:
    stub_user = StubUser()
    done = stub_user.find_more_than_equal_one({"name": "stub Guy 3"})
    assert done is list


def test_find_one() -> None:
    stub_user = StubUser()
    done = stub_user.find_one({"name": "stub Guy"})
    assert done is dict


class T(Enum):
    TESTE = 'teste'


def test_normalize_enum_types():
    payload = {'a': T.TESTE}
    BaseRepository.normalize_enum_types(payload=payload)
    assert payload == {'a': 'teste'}


def test_normalize_enum_types_deep():
    payload = {'a': {'b': T.TESTE}}
    BaseRepository.normalize_enum_types(payload=payload)
    assert payload == {'a': {'b': 'teste'}}
