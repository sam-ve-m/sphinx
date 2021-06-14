import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.views.service import ViewService
from tests.stub_classes.stub_base_repository import StubBaseRepository


class StubRepository(StubBaseRepository):
    pass


def test_create_register_exists():
    payload = {"name": "lala", "display_name": "Lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="^common.register_exists"):
        ViewService.create(payload=payload, view_repository=stub_repository)


def test_create_process_issue():
    payload = {"name": "lala", "display_name": "Lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        ViewService.create(payload=payload, view_repository=stub_repository)


def test_created():
    payload = {"name": "lala", "display_name": "Lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_repository.insert = MagicMock(return_value=True)
    response = ViewService.create(payload=payload, view_repository=stub_repository)
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "requests.created"


def test_update_register_not_exists():
    payload = {"view_id": "lala", "model": {"name": "lala", "display_name": "Lala"}}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        ViewService.update(payload=payload, view_repository=stub_repository)


def test_update_process_issue():
    payload = {"view_id": "lala", "model": {"name": "lala", "display_name": "Lala"}}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        ViewService.update(payload=payload, view_repository=stub_repository)


def test_updated():
    payload = {"view_id": "lala", "model": {"name": "lala", "display_name": "Lala"}}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=True)
    response = ViewService.update(payload=payload, view_repository=stub_repository)
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


def test_delete_register_not_exists():
    payload = {"view_id": "lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        ViewService.delete(payload=payload, view_repository=stub_repository)


def test_delete_process_issue():
    payload = {"view_id": "lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.delete_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        ViewService.delete(payload=payload, view_repository=stub_repository)


def test_deleted():
    payload = {"view_id": "lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.delete_one = MagicMock(return_value=True)
    response = ViewService.delete(payload=payload, view_repository=stub_repository)
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.deleted"


link_feature_payload = {"view_id": "lala", "feature_id": "lele"}


def test_link_feature_process_issue():
    view_repository = StubRepository(database="", collection="")
    feature_repository = StubRepository(database="", collection="")
    view_repository.find_one = MagicMock(return_value={"features": list()})
    feature_repository.find_one = MagicMock(return_value={})
    view_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        ViewService.link_feature(
            payload=link_feature_payload, view_repository=view_repository,
        )


def test_link_feature():
    view_repository = StubRepository(database="", collection="")
    feature_repository = StubRepository(database="", collection="")
    view_repository.find_one = MagicMock(return_value={"features": list()})
    feature_repository.find_one = MagicMock(return_value={})
    view_repository.update_one = MagicMock(return_value=True)
    response = ViewService.link_feature(
        payload=link_feature_payload, view_repository=view_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


def test_get_view_register_not_exists():
    payload = {"view_id": "lala"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        ViewService.get_view(payload=payload, view_repository=stub_repository)


def test_get_view():
    payload = {"view_id": "lala"}
    data = {"alala": "elele"}
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=data)
    response = ViewService.get_view(payload=payload, view_repository=stub_repository)
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == data
