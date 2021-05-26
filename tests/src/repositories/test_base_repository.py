from src.repositories.base_repository import BaseRepository
from pymongo.cursor import Cursor
from decouple import config
from unittest.mock import MagicMock


class StubbyUser(BaseRepository):

    def __init__(self) -> None:
        super().__init__(database=config('MONGODB_DATABASE_NAME'), collection=config('MONGODB_USER_COLLECTION'))


def test_insert_user() -> None:
    stubby_user = StubbyUser()
    stubby_user.insert = MagicMock(return_value=True)
    done = stubby_user.insert({"name": "stubby Guy"})
    assert done is True


def test_insert_many_users() -> None:
    stubby_user = StubbyUser()
    stubby_user.insert_many = MagicMock(return_value=True)
    done = stubby_user.insert_many([{"name": "stubby Guy 3"}, {"name": "stubby Guy 3"}])
    assert done is True


def test_find_many_users() -> None:
    stubby_user = StubbyUser()
    stubby_user.find_all = MagicMock(return_value=Cursor)
    done = stubby_user.find_all()
    assert done is Cursor

def test_find_more_then_one_equal_user() -> None:
    stubby_user = StubbyUser()
    stubby_user.find_more_than_equal_one = MagicMock(return_value=Cursor)
    done = stubby_user.find_more_than_equal_one({"name": "stubby Guy 3"})
    assert done is Cursor

def test_find_one() -> None:
    stubby_user = StubbyUser()
    stubby_user.find_one = MagicMock(return_value={})
    done = stubby_user.find_one({"name": "stubby Guy"})
    assert type(done) is dict
