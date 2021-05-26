from src.repositories.base_repository import BaseRepository
from decouple import config
import pytest
from pymongo.cursor import Cursor


class StubbyUser(BaseRepository):

    def __init__(self) -> None:
        super().__init__("lionx", "users")


def test_insert_user() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.insert({"name": "stubby Guy"})
    assert done is True


def test_insert_many_users() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.insert_many([{"name": "stubby Guy 3"}, {"name": "stubby Guy 3"}])
    assert done is True


def test_find_many_users() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.find_all()
    assert type(done) is Cursor

def test_find_more_then_one_equal_user() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.find_more_than_equal_one({"name": "stubby Guy 3"})
    assert type(done) is Cursor

def test_find_one() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.find_one({"name": "stubby Guy"})
    assert type(done) is dict
