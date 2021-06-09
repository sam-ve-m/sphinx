# OUTSIDE LIBRARIES
import pytest

# SPHINX
from src.utils.stone_age import StoneAge


def test_get_only_values_from_user_data():
    data = {
        "name": {"origin": "XXX", "value": "Andre"},
        "date": 123,
        "address": {
            "street": {"origin": "XXX", "value": "R. imbuia"},
            "number": {"origin": "XXX", "value": "153"},
        },
    }
    expected = {"name": "Andre", "date": 123, "address": {"street": "R. imbuia", "number": "153"}}
    result = StoneAge.get_only_values_from_user_data(user_data=data)
    assert expected == result
