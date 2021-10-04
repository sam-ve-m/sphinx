# Third part
import pytest

# Sphinx
from src.domain.model_decorator.generate_id import generate_id, hash_field


def test_generate_id_error_because_key_not_exists():
    with pytest.raises(Exception, match="Error to generate _id"):
        generate_id(
            key='lala',
            payload={},
            must_remove=False
        )


def test_generate_id_and_not_delete_the_key():
    payload = {'lala': 'oi'}
    generate_id(
        key='lala',
        payload=payload,
        must_remove=False
    )
    assert payload['lala'] == payload['_id']


def test_generate_id_and_delete_the_key():
    payload = {'lala': 'oi'}
    generate_id(
        key='lala',
        payload=payload,
        must_remove=True
    )
    assert 'oi' == payload['_id']
    assert payload.get('lala') == None


def test_generate_id_payload_as_str():
    with pytest.raises(AttributeError):
        generate_id(
            key='lala',
            payload='',
            must_remove=True
        )


def test_generate_id_key_as_dict():
    with pytest.raises(TypeError):
        generate_id(
            key={'teste': 123},
            payload={},
            must_remove=True
        )


def test_hash_field_str():
    value = 'oi'
    value = hash_field(
        payload=value
    )
    assert value == 'ef67e0868c98e5f0b0e2fcd9b0c4a3bad808f551'


def test_hash_field_dict():
    value = {'lala': 123}
    value = hash_field(
        payload=value,
        key='lala'
    )
    assert value['lala'] == '40bd001563085fc35165329ea1ff5c5ecbdbbeef'


def test_hash_field_dict_without_any_key():
    value = {'lala': 123}
    value = hash_field(
        payload=value
    )
    assert value == '80a8565af7ab52df7d911bd72d4b1c3018a4e835'