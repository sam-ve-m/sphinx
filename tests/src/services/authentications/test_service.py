import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)
from src.services.authentications.service import AuthenticationService
from tests.stub_classes.stub_base_repository import StubBaseRepository


class StubRepository(StubBaseRepository):
    pass


class StubTokenHandler(StubBaseRepository):
    @staticmethod
    def generate_token(paylod: dict, ttl: int):
        pass


class StubAuthenticationService:
    pass


payload = {"email": ""}


def test_answer_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.thebes_gate(
            payload=payload,
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
        )


def test_answer_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"is_active": False})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        AuthenticationService.thebes_gate(
            payload=payload,
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
        )


def test_answer_is_active():
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active": True}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        payload=payload,
        user_repository=stub_repository,
        token_handler=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == {"jwt": generate_token_value}


def test_answer_is_not_active():
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active": False}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        payload=payload,
        user_repository=stub_repository,
        token_handler=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == {"jwt": generate_token_value}


def test_login_not_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.login(
            payload=payload,
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
        )


def test_login_use_magic_link():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"use_magic_link": True})
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    AuthenticationService.login(
        payload=payload,
        user_repository=stub_repository,
        token_handler=StubTokenHandler,
    )


def test_login_without_pin():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"use_magic_link": False})
    response = AuthenticationService.login(
        payload=payload,
        user_repository=stub_repository,
        token_handler=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.need_pin"


def test_login_pin_error():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4sa390b0a572ac0d2c0220",
        }
    )
    with pytest.raises(UnauthorizedError, match="user.pin_error"):
        AuthenticationService.login(
            payload={"pin": "1234", "email": "lala"},
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
        )


def test_login_with_pin():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4a390b0a572ac0d2c0220",
        }
    )
    response = AuthenticationService.login(
        payload={"pin": "1234", "email": "lala"},
        user_repository=stub_repository,
        token_handler=StubTokenHandler,
    )

    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")


def test_forgot_password_not_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.login(
            payload=payload,
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
        )


def test_forgot_password():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = AuthenticationService.forgot_password(
        payload=payload, user_repository=stub_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.forgot_password"


class StubThebesHall:
    pass


def test_thebes_hall_not_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.thebes_hall(
            payload=payload,
            user_repository=stub_repository,
            token_handler=StubTokenHandler,
            thebes_hall=StubThebesHall,
        )


def test_thebes_hall():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    StubThebesHall.validate = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value="lallalala")
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = AuthenticationService.thebes_hall(
        payload=payload,
        user_repository=stub_repository,
        thebes_hall=StubThebesHall,
        token_handler=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")
