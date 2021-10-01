# OUTSIDE LIBRARIES

# SPHINX
from src.services.third_part_integration.stone_age import StoneAge


def test_get_only_values_from_user_data():
    data = {
        "name": {"source": "XXX", "value": "Andre"},
        "date": 123,
        "address": {
            "street": {"source": "XXX", "value": "R. imbuia"},
            "number": {"source": "XXX", "value": "153"},
        },
    }
    expected = {
        "name": "Andre",
        "date": 123,
        "address": {"street": "R. imbuia", "number": "153"},
    }
    result = StoneAge.get_only_values_from_user_data(user_data=data)
    assert expected == result
