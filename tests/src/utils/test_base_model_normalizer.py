# NATIVE LIBRARIES
from enum import Enum

# SPHINX
from src.utils.base_model_normalizer import normalize_enum_types


class T(Enum):
    TEST = "test"


def test_normalize_enum_types():
    payload = {"a": T.TEST}
    normalize_enum_types(payload=payload)
    assert payload == {"a": "test"}


def test_normalize_enum_types_deep():
    payload = {"a": {"b": T.TEST}}
    normalize_enum_types(payload=payload)
    assert payload == {"a": {"b": "test"}}