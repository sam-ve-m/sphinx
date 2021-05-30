import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.users.service import UserService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


class StubbyAuthenticationService:
    pass


class StubbyAuthenticationService:
    pass


payload = {"name": "lala", "email": "Lala", "pin": 1234}


def test_create_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="common.register_exists"):
        UserService.create(payload=payload, user_repository=stubby_repository)


def test_create_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.create(payload=payload, user_repository=stubby_repository)


def test_created():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=True)
    StubbyAuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = UserService.create(
        payload=payload,
        user_repository=stubby_repository,
        authentication_service=StubbyAuthenticationService,
    )
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "user.created"


payload_change_password = {"thebes_answer": {"email": "lalal"}, "new_pin": 1234}


def test_change_password_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_change_password_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_change_password():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.change_password(
        payload=payload_change_password, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


payload_change_view = {"thebes_answer": {"email": "lalal"}, "new_view": "lite"}


def test_change_view_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_change_view_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_change_view():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.change_view(
        payload=payload_change_view, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")


def test_delete_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.delete(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_delete_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.delete(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_delete():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.delete(
        payload=payload_change_view, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


def test_forgot_password_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_forgot_password():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    StubbyAuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = UserService.forgot_password(
        payload=payload_change_password, user_repository=stubby_repository, authentication_service=StubbyAuthenticationService
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "email.forgot_password"


def test_logout_all_not_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_logout_all_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={'email': 'lala'})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_logout_all():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={'email': 'lala'})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.logout_all(
        payload=payload_change_password, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.all_logged_out"
