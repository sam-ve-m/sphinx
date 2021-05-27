import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.users.service import UserService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


class StubbyEmailSender:
    @staticmethod
    def send_email_to(target_email: str, message: str, subject: str):
        pass


def test_create_invalid_params():
    private_payload = {"name": "", "email": ""}
    stubby_repository = StubbyRepository(database="", collection="")
    with pytest.raises(BadRequestError, match="common.invalid_params"):
        UserService.create(
            payload=private_payload,
            user_repository=stubby_repository,
            email_sender=StubbyEmailSender,
        )


payload = {"name": "lala", "email": "Lala", "pin": 1234}


def test_create_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="common.register_exists"):
        UserService.create(
            payload=payload,
            user_repository=stubby_repository,
            email_sender=StubbyEmailSender,
        )


def test_create_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.create(
            payload=payload,
            user_repository=stubby_repository,
            email_sender=StubbyEmailSender,
        )


def test_created():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=True)
    response = UserService.create(
        payload=payload,
        user_repository=stubby_repository,
        email_sender=StubbyEmailSender,
    )
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "user.created"
