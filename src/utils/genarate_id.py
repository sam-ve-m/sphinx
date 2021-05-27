from hashlib import sha1
from typing import Union


def generate_id(key: str, payload: dict, must_remove: bool = True) -> dict:
    _id = payload.get(key)
    if _id is None:
        raise Exception("Error to generate _id")
    payload.update({"_id": _id})
    if must_remove:
        del payload[key]
    return payload


def generate_list(key: str, payload: dict) -> dict:
    payload[key] = list()
    return payload


def hash_field(payload: Union[dict, str], key: str = None) -> dict:
    _sha1 = sha1()
    if key:
        _sha1.update(str(payload[key]).encode())
        payload[key] = _sha1.hexdigest()
    else:
        _sha1.update(str(payload).encode())
        payload = _sha1.hexdigest()
    return payload
