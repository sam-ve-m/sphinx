# Sphinx
from src.domain.model_decorator.generate_id import hash_field


def test_hash_field_str():
    value = "oi"
    value = hash_field(payload=value)
    assert value == "ef67e0868c98e5f0b0e2fcd9b0c4a3bad808f551"


def test_hash_field_dict():
    value = {"lala": 123}
    value = hash_field(payload=value, key="lala")
    assert value["lala"] == "40bd001563085fc35165329ea1ff5c5ecbdbbeef"


def test_hash_field_dict_without_any_key():
    value = {"lala": 123}
    value = hash_field(payload=value)
    assert value == "80a8565af7ab52df7d911bd72d4b1c3018a4e835"
