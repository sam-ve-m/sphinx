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
from tests.stub_classes.stub_persephone_service import StubPersephoneService


class StubRepository(StubBaseRepository):
    pass


class StubTokenHandler(StubBaseRepository):
    @staticmethod
    def generate_token(user_data: dict, ttl: int):
        pass


class StubAuthenticationService:
    pass


@pytest.fixture
def get_new_stub_persephone_service():
    stub_persephone_service = StubPersephoneService()
    return stub_persephone_service


payload_rec = {"x-thebes-answer": {"email": ""}}
payload = {"email": ""}


def test_answer_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
        )


def test_answer_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"is_active_user": False})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
        )


def test_answer_is_active_was_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": True}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        thebes_answer_from_request_or_error=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_answer_is_active_was_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": True}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        thebes_answer_from_request_or_error=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_answer_is_not_active_and_was_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": False}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    stub_persephone_service.run = MagicMock(return_value=True)
    response= AuthenticationService.thebes_gate(
        thebes_answer_from_request_or_error=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_answer_is_not_active_and_was_not_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": False}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )


def test_login_not_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.login(
            user_credentials=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
        )


def test_login_use_magic_link():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"use_magic_link": True})
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = AuthenticationService.login(
        user_credentials=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "email.login"


def test_login_without_pin():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"use_magic_link": False})
    response = AuthenticationService.login(
        user_credentials=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
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
    with pytest.raises(UnauthorizedError, match="^user.pin_error"):
        AuthenticationService.login(
            user_credentials={"pin": "1234", "email": "lala"},
            user_repository=stub_repository,
            token_service=StubTokenHandler,
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
        user_credentials={"pin": "1234", "email": "lala"},
        user_repository=stub_repository,
        token_service=StubTokenHandler,
    )

    assert response.get("status_code") == status.HTTP_200_OK


class StubThebesHall:
    pass


def test_thebes_hall_not_register_exists_was_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_persephone_service.run = MagicMock(return_value=True)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )


def test_thebes_hall_not_register_exists_was_not_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )


def test_thebes_hall_was_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    StubThebesHall.validate = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value="lallalala")
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    AuthenticationService._dtvm_client_has_trade_allowed = MagicMock(return_value={})
    stub_persephone_service.run = MagicMock(return_value=True)
    response = AuthenticationService.thebes_hall(
        device_and_thebes_answer_from_request=payload_rec,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_thebes_hall_was_not_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    StubThebesHall.validate = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value="lallalala")
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    stub_persephone_service.run = MagicMock(return_value=False)
    AuthenticationService._dtvm_client_has_trade_allowed = MagicMock(return_value={})
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )

