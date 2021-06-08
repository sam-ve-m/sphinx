import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)
from src.services.authentications.service import AuthenticationService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


class StubbyTokenHandler(StubbyBaseRepository):
    @staticmethod
    def generate_token(paylod: dict, ttl: int):
        pass


class StubbyAuthenticationService:
    pass


payload = {"email": ""}


def test_answer_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.thebes_gate(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_answer_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"is_active": False})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        AuthenticationService.thebes_gate(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_answer_is_active():
    generate_token_value = "lalala"
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active": True}
    )
    stubby_repository.update_one = MagicMock(return_value=True)
    StubbyTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        payload=payload,
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == {"jwt": generate_token_value}


def test_answer_is_not_active():
    generate_token_value = "lalala"
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active": False}
    )
    stubby_repository.update_one = MagicMock(return_value=True)
    StubbyTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        payload=payload,
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == {"jwt": generate_token_value}


def test_login_not_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.login(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_login_use_magic_link():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"use_magic_link": True})
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    AuthenticationService.login(
        payload=payload,
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )


def test_login_without_pin():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"use_magic_link": False})
    response = AuthenticationService.login(
        payload=payload,
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.need_pin"


def test_login_pin_error():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4sa390b0a572ac0d2c0220",
        }
    )
    with pytest.raises(UnauthorizedError, match="user.pin_error"):
        AuthenticationService.login(
            payload={"pin": "1234", "email": "lala"},
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_login_with_pin():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4a390b0a572ac0d2c0220",
        }
    )
    response = AuthenticationService.login(
        payload={"pin": "1234", "email": "lala"},
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )

    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")


def test_forgot_password_not_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.login(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_forgot_password():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = AuthenticationService.forgot_password(
        payload=payload, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.forgot_password"


class StubbyThebesHall:
    pass


def test_thebes_hall_not_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.thebes_hall(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
            thebes_hall=StubbyThebesHall,
        )


def test_thebes_hall():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    StubbyThebesHall.validate = MagicMock(return_value=True)
    StubbyTokenHandler.generate_token = MagicMock(return_value="lallalala")
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = AuthenticationService.thebes_hall(
        payload=payload,
        user_repository=stubby_repository,
        thebes_hall=StubbyThebesHall,
        token_handler=StubbyTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")
