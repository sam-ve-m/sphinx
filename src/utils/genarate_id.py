
def generate_id(key: str, payload: dict) -> dict:
    _id = payload.get(key)
    if _id is None:
        raise Exception('Error to generate _id')
    payload.update({'_id': _id})
    return payload
