# STANDARD LIBS
from enum import Enum


def normalize_enum_types(payload: dict):
    for key in payload:
        if key == 'modified_register_data':
            print(payload)
        if isinstance(payload[key], Enum):
            payload[key] = payload[key].value
        elif type(payload[key]) == dict:
            normalize_enum_types(payload=payload[key])
        elif type(payload[key]) == list:
            for item in payload[key]:
                if type(item) == dict:
                    normalize_enum_types(item)
