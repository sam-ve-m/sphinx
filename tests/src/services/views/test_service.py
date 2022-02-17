# STANDARD LIBS


# OUTSIDE LIBRARIES
from fastapi import status
from unittest.mock import MagicMock
import pytest

# SPHINX
from src.services.views.service import ViewService
from src.exceptions.exceptions import BadRequestError, InternalServerError


class StubViewRepository:
    pass


def test_create_register_already_exists():
    with pytest.raises(BadRequestError, match="common.register_exists"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value={})
        ViewService.create(
            payload={"name": "test"}, view_repository=stub_view_repository
        )


def test_create_error_on_save():
    with pytest.raises(InternalServerError, match="common.process_issue"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value=None)
        stub_view_repository.insert = MagicMock(return_value=False)
        ViewService.create(
            payload={"name": "test"}, view_repository=stub_view_repository
        )


def test_create():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value=None)
    stub_view_repository.insert = MagicMock(return_value=True)
    result = ViewService.create(
        payload={"name": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_201_CREATED
    assert result["message_key"] == "requests.created"


def test_update_register_not_exists():
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value=None)
        ViewService.update(payload={"model": {}}, view_repository=stub_view_repository)


def test_update_error_on_save():
    with pytest.raises(InternalServerError, match="common.process_issue"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value={})
        stub_view_repository.update_one = MagicMock(return_value=False)
        ViewService.update(payload={"model": {}}, view_repository=stub_view_repository)


def test_update():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={})
    stub_view_repository.update_one = MagicMock(return_value=True)
    result = ViewService.update(
        payload={"model": {}}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_200_OK
    assert result["message_key"] == "requests.updated"


def test_delete_register_already_exists():
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value=None)
        ViewService.delete(
            payload={"model": "test"}, view_repository=stub_view_repository
        )


def test_delete_error_on_save():
    with pytest.raises(InternalServerError, match="common.process_issue"):
        stub_view_repository = StubViewRepository()
        stub_view_repository.find_one = MagicMock(return_value={})
        stub_view_repository.delete_one = MagicMock(return_value=False)
        ViewService.delete(
            payload={"name": "test"}, view_repository=stub_view_repository
        )


def test_delete():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={})
    stub_view_repository.delete_one = MagicMock(return_value=True)
    result = ViewService.delete(
        payload={"name": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_200_OK
    assert result["message_key"] == "requests.deleted"


def test_link_feature_register_not_exist():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value=None)
    stub_view_repository.update_one = MagicMock(return_value=True)
    result = ViewService.link_feature(
        payload={"name": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_304_NOT_MODIFIED
    assert result["message_key"] == "requests.not_modified"


def test_link_feature_register_exist_feature_already_in():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={"features": ["test"]})
    stub_view_repository.update_one = MagicMock(return_value=True)
    result = ViewService.link_feature(
        payload={"feature_id": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_304_NOT_MODIFIED
    assert result["message_key"] == "requests.not_modified"


def test_link_feature_register_exist_feature_not_in_error_on_update():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={"features": []})
    stub_view_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        ViewService.link_feature(
            payload={"feature_id": "test"}, view_repository=stub_view_repository
        )


def test_link_feature():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={"features": []})
    stub_view_repository.update_one = MagicMock(return_value=True)
    result = ViewService.link_feature(
        payload={"feature_id": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_200_OK
    assert result["message_key"] == "requests.updated"


def test_get_view_register_nor_exists():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value=None)
    stub_view_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        ViewService.get_view(
            payload={"view_id": "test"}, view_repository=stub_view_repository
        )


def test_get_view():
    stub_view_repository = StubViewRepository()
    stub_view_repository.find_one = MagicMock(return_value={})
    stub_view_repository.update_one = MagicMock(return_value=False)
    result = ViewService.get_view(
        payload={"view_id": "test"}, view_repository=stub_view_repository
    )
    assert result["status_code"] == status.HTTP_200_OK
    assert result["payload"] is not None
