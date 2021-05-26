import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import (BadRequestError, InternalServerError)
from src.services.views.service import ViewService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


def test_create_invalid_params():
    payload = {
        'name': '',
        'display_name': ''
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        ViewService.create(payload=payload, view_repository=stubby_repository)


def test_create_register_exists():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match='common.register_exists'):
        ViewService.create(payload=payload, view_repository=stubby_repository)


def test_create_process_issue():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        ViewService.create(payload=payload, view_repository=stubby_repository)


def test_created():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=True)
    response = ViewService.create(payload=payload, view_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_201_CREATED
    assert response.get('message_key') == 'requests.created'


def test_update_invalid_params():
    payload = {
        'view_id': '',
        'model': {
            'name': '',
            'display_name': ''
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        ViewService.update(payload=payload, view_repository=stubby_repository)


def test_update_register_not_exists():
    payload = {
        'view_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        ViewService.update(payload=payload, view_repository=stubby_repository)


def test_update_process_issue():
    payload = {
        'view_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        ViewService.update(payload=payload, view_repository=stubby_repository)


def test_updated():
    payload = {
        'view_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = ViewService.update(payload=payload, view_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('message_key') == 'requests.updated'


def test_delete_invalid_params():
    payload = {
        'view_id': '',
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        ViewService.delete(payload=payload, view_repository=stubby_repository)


def test_delete_register_not_exists():
    payload = {
        'view_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        ViewService.delete(payload=payload, view_repository=stubby_repository)


def test_delete_process_issue():
    payload = {
        'view_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.delete_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        ViewService.delete(payload=payload, view_repository=stubby_repository)


def test_deleted():
    payload = {
        'view_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.delete_one = MagicMock(return_value=True)
    response = ViewService.delete(payload=payload, view_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('message_key') == 'requests.deleted'


def test_link_feature_invalid_params():
    payload = {
        'view_id': '',
        'feature_id': ''
    }
    stubby_repository = StubbyRepository(database='', collection='')
    feature_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        ViewService.link_feature(
            payload=payload,
            view_repository=stubby_repository,
            feature_repository=feature_repository
        )


link_feature_payload = {
    'view_id': 'lala',
    'feature_id': 'lele'
}


def test_link_feature_register_not_exists_view():
    view_repository = StubbyRepository(database='', collection='')
    feature_repository = StubbyRepository(database='', collection='')
    view_repository.find_one = MagicMock(return_value=None)
    feature_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        ViewService.link_feature(
            payload=link_feature_payload,
            view_repository=view_repository,
            feature_repository=feature_repository
        )


def test_link_feature_register_not_exists_feature():
    view_repository = StubbyRepository(database='', collection='')
    feature_repository = StubbyRepository(database='', collection='')
    view_repository.find_one = MagicMock(return_value={})
    feature_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='view.feature_not_exists'):
        ViewService.link_feature(
            payload=link_feature_payload,
            view_repository=view_repository,
            feature_repository=feature_repository
        )


def test_link_feature_process_issue():
    view_repository = StubbyRepository(database='', collection='')
    feature_repository = StubbyRepository(database='', collection='')
    view_repository.find_one = MagicMock(return_value={'features': list()})
    feature_repository.find_one = MagicMock(return_value={})
    view_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        ViewService.link_feature(
            payload=link_feature_payload,
            view_repository=view_repository,
            feature_repository=feature_repository
        )


def test_link_feature():
    view_repository = StubbyRepository(database='', collection='')
    feature_repository = StubbyRepository(database='', collection='')
    view_repository.find_one = MagicMock(return_value={'features': list()})
    feature_repository.find_one = MagicMock(return_value={})
    view_repository.update_one = MagicMock(return_value=True)
    response = ViewService.link_feature(
            payload=link_feature_payload,
            view_repository=view_repository,
            feature_repository=feature_repository
        )
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('message_key') == 'requests.updated'


def test_get_view_invalid_params():
    payload = {
        'view_id': '',
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        ViewService.get_view(payload=payload, view_repository=stubby_repository)


def test_get_view_register_not_exists():
    payload = {
        'view_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        ViewService.get_view(payload=payload, view_repository=stubby_repository)


def test_get_view():
    payload = {
        'view_id': 'lala'
    }
    data = {
        'alala': 'elele'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=data)
    response = ViewService.get_view(payload=payload, view_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('payload') == data