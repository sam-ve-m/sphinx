# STANDARD LIBS
from enum import Enum

# OUTSIDE LIBRARIES
from unittest.mock import MagicMock

# SPHINX
from src.repositories.base_repository import BaseRepository


class StubMongoCollection:
    pass


class StubCache:
    pass


class StubBaseRepository(BaseRepository):
    client = None

    def __init__(self, collection: StubMongoCollection) -> None:
        self.collection = collection


def test_insert_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.insert_one = MagicMock(side_effect=Exception())
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert (
        stub_base_repository.insert(
            data={"test_insert_user_false": "test_insert_user_false"}
        )
        is False
    )


def test_insert_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.insert_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.insert(
        data={"test_insert_user_false": "test_insert_user_false"}
    )


def test_insert_many_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.insert_many = MagicMock(side_effect=Exception())
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.insert_many(data=["test_insert_user_false"]) is False


def test_insert_many_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.insert_many = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.insert_many(data=["test_insert_user_false"])


def test_find_one_false_without_cache() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(side_effect={})
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository._get_from_cache = MagicMock(return_value=False)
    stub_cache = StubCache()
    assert (
        stub_base_repository.find_one(
            query={"test_insert_user_false": "test_insert_user_false"},
            cache=stub_cache,
        )
        is None
    )


def test_find_one_true_without_cache() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(return_value={"source":"collection"})
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository._get_from_cache = MagicMock(return_value={"source":"redis"})
    stub_base_repository.find_one = MagicMock(return_value={"source": "collection"})
    stub_cache = StubCache()
    from_source = stub_base_repository.find_one(
        query={"test_insert_user_false": "test_insert_user_false"}, ttl=0, cache=stub_cache,
    )
    assert type(from_source) == dict


def test_find_one_true_with_cache() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(return_value={})
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository._get_from_cache = MagicMock(return_value={"source":"redis"})
    stub_cache = StubCache()
    from_source = stub_base_repository.find_one(
            query={"test_insert_user_false": "test_insert_user_false"},
            ttl=2,
            cache=stub_cache,
        )
    assert type(from_source) == dict


def test_find_more_than_equal_one_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find = MagicMock(side_effect=Exception())
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert (
        stub_base_repository.find_more_than_equal_one(
            query={"test_insert_user_false": "test_insert_user_false"}
        )
        is None
    )


def test_find_more_than_equal_one_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.find_more_than_equal_one(
        query={"test_insert_user_false": "test_insert_user_false"}
    )


def test_find_all_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find = MagicMock(side_effect=Exception())
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.find_all() is None


def test_find_all_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.find_all()


def test_update_one_expect_false_because_is_none() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old=None, new=None)
    assert response is False


def test_update_one_expect_false_because_is_blank_object() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={}, new={})
    assert response is False


def test_update_one_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={}, new={})
    assert response is False


def test_update_one_expect_false_because_one_is_blank_object_v1() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={"oi": 12}, new={})
    assert response is False


def test_update_one_expect_false_because_one_is_none_v1() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={"oi": 12}, new=None)
    assert response is False


def test_update_one_expect_false_because_one_is_blank_object_v2() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={}, new={"oi": 12})
    assert response is False


def test_update_one_expect_false_because_one_is_none_v2() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old=None, new={"oi": 12})
    assert response is False


def test_update_one_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.update_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    response = stub_base_repository.update_one(old={"oi": 12}, new={"oi": 12})
    assert response


def test_delete_one_false() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.delete_one = MagicMock(side_effect=Exception())
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.delete_one(entity={}) is False


def test_delete_one_true() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.delete_one = MagicMock(return_value=True)
    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    assert stub_base_repository.delete_one(entity={})


class T(Enum):
    TEST = "test"


def test_normalize_enum_types():
    payload = {"a": T.TEST}
    stub_mongo_collection = StubMongoCollection()
    base_repository = StubBaseRepository(collection=stub_mongo_collection)
    base_repository.normalize_enum_types(payload=payload)
    assert payload == {"a": "test"}


def test_normalize_enum_types_deep():
    payload = {"a": {"b": T.TEST}}
    stub_mongo_collection = StubMongoCollection()
    base_repository = StubBaseRepository(collection=stub_mongo_collection)
    base_repository.normalize_enum_types(payload=payload)
    assert payload == {"a": {"b": "test"}}


def test__get_from_cache_not_cached() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(return_value=True)

    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository.base_identifier = "test"
    stub_cache = StubCache()
    stub_cache.get = MagicMock(return_value=None)
    stub_cache.set = MagicMock(return_value=None)
    assert stub_base_repository._get_from_cache(
        query={"test_insert_user_false": "test_insert_user_false"},
        cache=stub_cache,
    ) is None


def test__get_from_cache_query_is_none() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(return_value=True)

    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository.base_identifier = "test"
    stub_cache = StubCache()
    stub_cache.get = MagicMock(return_value=None)
    stub_cache.set = MagicMock(return_value=None)
    assert stub_base_repository._get_from_cache(
        query=None,
        cache=stub_cache,
    ) is None


def test__get_from_cache_cached() -> None:
    stub_mongo_collection = StubMongoCollection()
    stub_mongo_collection.find_one = MagicMock(return_value=True)

    stub_base_repository = StubBaseRepository(collection=stub_mongo_collection)
    stub_base_repository.base_identifier = "test"
    stub_cache = StubCache()
    stub_cache.get = MagicMock(return_value={"test__get_from_cache_cached": 1})
    stub_cache.set = MagicMock(return_value=None)
    assert stub_base_repository._get_from_cache(
        query={"test_insert_user_false": "test_insert_user_false"},
        cache=stub_cache,
    ) == {"test__get_from_cache_cached": 1}
