from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository
from decouple import config
from unittest.mock import MagicMock


class StubbyUser(StubbyBaseRepository):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_USER_COLLECTION"),
        )


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
    done = stubby_user.find_all()
    assert done is list


def test_find_more_then_one_equal_user() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.find_more_than_equal_one({"name": "stubby Guy 3"})
    assert done is list


def test_find_one() -> None:
    stubby_user = StubbyUser()
    done = stubby_user.find_one({"name": "stubby Guy"})
    assert done is dict
