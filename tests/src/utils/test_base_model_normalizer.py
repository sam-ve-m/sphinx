# NATIVE LIBRARIES
from enum import Enum

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class StubMongoCollection:
    pass


class StubMongoDBInfrastructure(MongoDBInfrastructure):
    client = None

    def __init__(self, collection: StubMongoCollection) -> None:
        self.collection = collection


class T(Enum):
    TEST = "test"


def test_normalize_enum_types():
    payload = {"a": T.TEST}
    stub_mongo_collection = StubMongoCollection()
    base_repository = StubMongoDBInfrastructure(collection=stub_mongo_collection)
    base_repository.normalize_enum_types(payload=payload)
    assert payload == {"a": "test"}


def test_normalize_enum_types_deep():
    payload = {"a": {"b": T.TEST}}
    stub_mongo_collection = StubMongoCollection()
    base_repository = StubMongoDBInfrastructure(collection=stub_mongo_collection)
    base_repository.normalize_enum_types(payload=payload)
    assert payload == {"a": {"b": "test"}}