import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import (BadRequestError, InternalServerError)
from src.services.features.service import FeatureService
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
        FeatureService.create(payload=payload, feature_repository=stubby_repository)


def test_create_register_exists():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match='common.register_exists'):
        FeatureService.create(payload=payload, feature_repository=stubby_repository)


def test_create_process_issue():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        FeatureService.create(payload=payload, feature_repository=stubby_repository)


def test_created():
    payload = {
        'name': 'lala',
        'display_name': 'Lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=True)
    response = FeatureService.create(payload=payload, feature_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_201_CREATED
    assert response.get('message_key') == 'requests.created'


def test_update_invalid_params():
    payload = {
        'feature_id': '',
        'model': {
            'name': '',
            'display_name': ''
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        FeatureService.update(payload=payload, feature_repository=stubby_repository)


def test_update_register_not_exists():
    payload = {
        'feature_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        FeatureService.update(payload=payload, feature_repository=stubby_repository)


def test_update_process_issue():
    payload = {
        'feature_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        FeatureService.update(payload=payload, feature_repository=stubby_repository)


def test_updated():
    payload = {
        'feature_id': 'lala',
        'model': {
            'name': 'lala',
            'display_name': 'Lala'
        }
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = FeatureService.update(payload=payload, feature_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('message_key') == 'requests.updated'


def test_delete_invalid_params():
    payload = {
        'feature_id': '',
    }
    stubby_repository = StubbyRepository(database='', collection='')
    with pytest.raises(BadRequestError, match='common.invalid_params'):
        FeatureService.delete(payload=payload, feature_repository=stubby_repository)


def test_delete_register_not_exists():
    payload = {
        'feature_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match='common.register_not_exists'):
        FeatureService.delete(payload=payload, feature_repository=stubby_repository)


def test_delete_process_issue():
    payload = {
        'feature_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.delete_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match='common.process_issue'):
        FeatureService.delete(payload=payload, feature_repository=stubby_repository)


def test_deleted():
    payload = {
        'feature_id': 'lala'
    }
    stubby_repository = StubbyRepository(database='', collection='')
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.delete_one = MagicMock(return_value=True)
    response = FeatureService.delete(payload=payload, feature_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_200_OK
    assert response.get('message_key') == 'requests.deleted'
