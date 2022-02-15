from hashlib import sha1
from typing import Union
from uuid import uuid4


def generate_unique_id(key: str, payload: dict) -> dict:
    payload.update({"unique_id": str(uuid4())})
    return payload


async def hash_field(payload: Union[dict, str], key: str = None) -> dict:
    _sha1 = sha1()
    if key:
        _sha1.update(str(payload[key]).encode())
        payload[key] = _sha1.hexdigest()
    else:
        _sha1.update(str(payload).encode())
        payload = _sha1.hexdigest()
    return payload
