import pytest
from unittest.mock import MagicMock, patch
from fastapi import status

from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)
from src.services.authentications.service import AuthenticationService
from tests.stub_classes.stub_base_repository import StubBaseRepository
from tests.stub_classes.stub_persephone_service import StubPersephoneService
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from tests.stub_classes.stub_jwt_service_composition import StubJwtService


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


@pytest.fixture
def get_authentication_service():
    authentication_service = AuthenticationService()
    return authentication_service


@pytest.fixture
def get_authentication_service_mock_send_authentication_email():
    AuthenticationService.send_authentication_email = MagicMock(return_value=True)
    return AuthenticationService


@pytest.fixture
def get_new_stub_jwt_service():
    stub_jwt_service = StubJwtService()
    return stub_jwt_service


payload_rec = {"x-thebes-answer": {"email": ""}}
payload = {"email": ""}


def test_thebes_gate_answer_register_not_exists(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service,
        )


def test_thebes_gate_answer_is_not_active_process_issue_on_update_user_data(
    get_new_stub_persephone_service,
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"is_active_user": False})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service,
        )


def test_thebes_gate_answer_is_not_active_process_issue_on_sent_to_persephone(
    get_new_stub_persephone_service,
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"is_active_user": False})
    stub_repository.update_one = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service,
        )


def test_thebes_gate_answer_is_not_active(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": False}
    )
    stub_repository.update_one = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        thebes_answer_from_request_or_error=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service,
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_thebes_gate_answer_is_active_was_sent_to_persephone(
    get_new_stub_persephone_service,
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    generate_token_value = "lalala"
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={"pin": "", "_id": "", "is_active_user": True}
    )
    stub_repository.update_one = MagicMock(return_value=False)
    StubTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.thebes_gate(
        thebes_answer_from_request_or_error=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service,
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_thebes_gate_answer_is_active_process_issue_on_sent_to_persephone(
    get_new_stub_persephone_service,
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"is_active_user": True})
    stub_repository.update_one = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=payload,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service,
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


def test_login_use_magic_link(get_authentication_service_mock_send_authentication_email):
    authentication_service = get_authentication_service_mock_send_authentication_email
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={
        "use_magic_link": True,
        "email": ''
    })
    response = authentication_service.login(
        user_credentials=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "email.login"


def test_login_without_pin():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={
        "use_magic_link": False,
        "email": ''
    })
    response = AuthenticationService.login(
        user_credentials=payload,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.need_pin"


def test_login_pin_error_1():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4sa390b0a572ac0d2c0220",
            "email": ''
        }
    )
    with pytest.raises(UnauthorizedError, match="^user.pin_error"):
        AuthenticationService.login(
            user_credentials={"pin": "1234", "email": "lala"},
            user_repository=stub_repository,
            token_service=StubTokenHandler,
        )



def test_login_pin_error_2():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4sa390b0a572ac0d2c0220",
            "email": ''
        }
    )
    with pytest.raises(UnauthorizedError, match="^user.pin_error"):
        AuthenticationService.login(
            user_credentials={"pin": "4321", "email": "lala"},
            user_repository=stub_repository,
            token_service=StubTokenHandler,
        )


def test_login_with_pin():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(
        return_value={
            "use_magic_link": False,
            "pin": "7110eda4d09e062aa5e4a390b0a572ac0d2c0220",
            "email": ''
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


def test_thebes_hall_not_register_exists(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_persephone_service.run = MagicMock(return_value=True)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service,
        )


@patch('src.services.authentications.service.AuthenticationService._dtvm_client_has_trade_allowed')
def test_thebes_hall_muts_update_and_raise_error_on_update(
        mock_dtvm_client_has_trade_allowed,
        get_new_stub_persephone_service,
        get_authentication_service
):
    authentication_service = get_authentication_service
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=False)
    authentication_service.send_authentication_email = MagicMock(return_value=True)
    mock_dtvm_client_has_trade_allowed.return_value = {
        "solutiontech": {
            "status": 'changed',
            "status_changed": True,
        }
    }
    stub_persephone_service.run = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        authentication_service.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )


@patch('src.services.authentications.service.AuthenticationService._dtvm_client_has_trade_allowed')
def test_thebes_hall_muts_update_dont_sent_to_persephone(
        mock_dtvm_client_has_trade_allowed,
        get_new_stub_persephone_service,
        get_authentication_service
):
    authentication_service = get_authentication_service
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=True)
    authentication_service.send_authentication_email = MagicMock(return_value=True)
    mock_dtvm_client_has_trade_allowed.return_value = {
        "solutiontech": {
            "status": 'changed',
            "status_changed": True,
        }
    }
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        authentication_service.thebes_hall(
            device_and_thebes_answer_from_request=payload_rec,
            user_repository=stub_repository,
            token_service=StubTokenHandler,
            persephone_client=stub_persephone_service
        )


@patch('src.services.authentications.service.AuthenticationService._dtvm_client_has_trade_allowed')
def test_thebes_hall_was_sent_to_persephone(
        mock_dtvm_client_has_trade_allowed,
        get_new_stub_persephone_service,
        get_authentication_service
):
    authentication_service = get_authentication_service
    stub_persephone_service = get_new_stub_persephone_service
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    StubThebesHall.validate = MagicMock(return_value=True)
    StubTokenHandler.generate_token = MagicMock(return_value="lallalala")
    authentication_service.send_authentication_email = MagicMock(return_value=True)
    mock_dtvm_client_has_trade_allowed.return_value = {
        "solutiontech": {
            "status": 'changed',
            "status_changed": False,
        }
    }
    stub_persephone_service.run = MagicMock(return_value=True)
    response = authentication_service.thebes_hall(
        device_and_thebes_answer_from_request=payload_rec,
        user_repository=stub_repository,
        token_service=StubTokenHandler,
        persephone_client=stub_persephone_service
    )
    assert response.get("status_code") == status.HTTP_200_OK


def test_update_client_has_trade_allowed_status_with_solutiontech_status_response_change():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=True,
            user_sinacor_status_from_database=True,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_solutiontech_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        user_solutiontech_status_from_database='t1',
        user_solutiontech_status_from_check_status_request='t2'
    )
    assert client_has_trade_allowed_status_with_database_user["solutiontech"]["status"] == 't2'
    assert client_has_trade_allowed_status_with_database_user["solutiontech"]["status_changed"] is True


def test_update_client_has_trade_allowed_status_with_solutiontech_status_response_dont_change():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=True,
            user_sinacor_status_from_database=True,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_solutiontech_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        user_solutiontech_status_from_database='t1',
        user_solutiontech_status_from_check_status_request='t1'
    )
    assert client_has_trade_allowed_status_with_database_user["solutiontech"]["status"] == 't1'
    assert client_has_trade_allowed_status_with_database_user["solutiontech"]["status_changed"] is False


def test_update_client_has_trade_allowed_status_with_sincad_status_response_change_to_true():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=False,
            user_sinacor_status_from_database=True,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        sincad_status_from_sinacor=True,
        user_sincad_status_from_database=False
    )
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status"] is True
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status_changed"] is True


def test_update_client_has_trade_allowed_status_with_sincad_status_response_change_to_false():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=True,
            user_sinacor_status_from_database=False,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        sincad_status_from_sinacor=False,
        user_sincad_status_from_database=True
    )
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status"] is False
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status_changed"] is True


def test_update_client_has_trade_allowed_status_with_sincad_status_response_dont_change():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=True,
            user_sinacor_status_from_database=True,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        sincad_status_from_sinacor=True,
        user_sincad_status_from_database=True
    )
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status"] is True
    assert client_has_trade_allowed_status_with_database_user["sincad"]["status_changed"] is False


def test_update_client_has_trade_allowed_status_with_sinacor_status_response_change():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=False,
            user_sinacor_status_from_database=False,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_sinacor_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        sinacor_status_from_sinacor=True,
        user_sinacor_status_from_database=False
    )
    assert client_has_trade_allowed_status_with_database_user["sinacor"]["status"] is True
    assert client_has_trade_allowed_status_with_database_user["sinacor"]["status_changed"] is True


def test_update_client_has_trade_allowed_status_with_sinacor_status_response_dont_change():
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database='t1',
            user_sincad_status_from_database=True,
            user_sinacor_status_from_database=True,
        )
    )
    AuthenticationService._update_client_has_trade_allowed_status_with_sinacor_status_response(
        client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
        sinacor_status_from_sinacor=True,
        user_sinacor_status_from_database=True
    )
    assert client_has_trade_allowed_status_with_database_user["sinacor"]["status"] is True
    assert client_has_trade_allowed_status_with_database_user["sinacor"]["status_changed"] is False


def test_check_if_user_has_valid_solutiontech_status_in_database_send_status():
    assert AuthenticationService.check_if_user_has_valid_solutiontech_status_in_database(
        user_solutiontech_status_from_database=SolutiontechClientImportStatus.SEND.value
    )


def test_check_if_user_has_valid_solutiontech_status_in_database_failed_status():
    assert AuthenticationService.check_if_user_has_valid_solutiontech_status_in_database(
        user_solutiontech_status_from_database=SolutiontechClientImportStatus.SEND.value
    )


def test_check_if_user_has_valid_solutiontech_status_in_database_sync_status():
    assert AuthenticationService.check_if_user_has_valid_solutiontech_status_in_database(
        user_solutiontech_status_from_database=SolutiontechClientImportStatus.SYNC.value
    ) is False


class StubClientRegisterRepository:
    pass


def test_sinacor_is_synced_with_sincad_empty_return():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=None)
    assert AuthenticationService.sinacor_is_synced_with_sincad(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is None


def test_sinacor_is_synced_with_sincad_not_synced():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('AAA',))
    assert AuthenticationService.sinacor_is_synced_with_sincad(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is False


def test_sinacor_is_synced_with_sincad_synced():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    assert AuthenticationService.sinacor_is_synced_with_sincad(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is True


def test_client_sinacor_is_blocked_empty_return():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=None)
    assert AuthenticationService.client_sinacor_is_blocked(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is None


def test_client_sinacor_is_blocked_not_synced():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('AAA',))
    assert AuthenticationService.client_sinacor_is_blocked(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is False


def test_client_sinacor_is_blocked_synced():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    assert AuthenticationService.client_sinacor_is_blocked(
        user_cpf=1234567890,
        client_register_repository=stub_client_register_repository
    ) is True


class StubSolutiontech:
    pass


def test_dtvm_client_has_trade_allowed_synced_solutiontech_synced_sincad_synced_sinacor():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SYNC.value,
        "sincad": True,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': False},
        'sincad': {'status': True, 'status_changed': False},
        'sinacor': {'status': True, 'status_changed': False}
    }


def test_dtvm_client_has_trade_allowed_not_synced_solutiontech_synced_sincad_synced_sinacor():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SEND.value,
        "sincad": True,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': True},
        'sincad': {'status': True, 'status_changed': False},
        'sinacor': {'status': True, 'status_changed': False}
    }


def test_dtvm_client_has_trade_allowed_not_synced_solutiontech_not_synced_sincad_synced_sinacor():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SEND.value,
        "sincad": False,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': True},
        'sincad': {'status': True, 'status_changed': True},
        'sinacor': {'status': True, 'status_changed': False}
    }


def test_dtvm_client_has_trade_allowed_not_synced_solutiontech_not_synced_sincad_not_synced_sinacor():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SEND.value,
        "sincad": False,
        "sinacor": False,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': True},
        'sincad': {'status': True, 'status_changed': True},
        'sinacor': {'status': True, 'status_changed': True}
    }


def test_dtvm_client_has_trade_allowed_synced_solutiontech_synced_sincad_synced_sinacor_change_solutiontech_status():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SYNC.value,
        "sincad": True,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.FAILED.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': False},
        'sincad': {'status': True, 'status_changed': False},
        'sinacor': {'status': True, 'status_changed': False}
    }


def test_dtvm_client_has_trade_allowed_synced_solutiontech_synced_sincad_synced_sinacor_change_sincad_status():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SYNC.value,
        "sincad": True,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('AAA',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('A',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': False},
        'sincad': {'status': True, 'status_changed': False},
        'sinacor': {'status': True, 'status_changed': False}
    }


def test_dtvm_client_has_trade_allowed_synced_solutiontech_synced_sincad_synced_sinacor_change_sinacor_status():
    user = {
        "solutiontech": SolutiontechClientImportStatus.SYNC.value,
        "sincad": True,
        "sinacor": True,
        "bmf_account": 1,
        "cpf": 12345678900
    }
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_sincad_status = MagicMock(return_value=('ACE',))
    stub_client_register_repository.get_sinacor_status = MagicMock(return_value=('B',))
    stub_solutiontech = StubSolutiontech()
    stub_solutiontech.check_if_client_is_synced_with_solutiontech = MagicMock(
        return_value=SolutiontechClientImportStatus.SYNC.value
    )
    client_has_trade_allowed_status_with_database_user = (
        AuthenticationService._dtvm_client_has_trade_allowed(
            user=user,
            client_register_repository=stub_client_register_repository,
            solutiontech=stub_solutiontech
        )
    )
    assert client_has_trade_allowed_status_with_database_user == {
        'solutiontech': {'status': 'sync', 'status_changed': False},
        'sincad': {'status': True, 'status_changed': False},
        'sinacor': {'status': False, 'status_changed': True}
    }


def test_create_electronic_signature_jwt_failed_to_generate_session_and_send_to_persephone(
    get_new_stub_persephone_service,
    get_new_stub_jwt_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_jwt_service = get_new_stub_jwt_service
    stub_jwt_service.generate_session_jwt = MagicMock(side_effect=UnauthorizedError())
    stub_persephone_service.run = MagicMock(return_value=True)
    with pytest.raises(UnauthorizedError):
        AuthenticationService.create_electronic_signature_jwt(
            change_electronic_signature_request={
                "electronic_signature": "",
                "email": "",
            },
            persephone_client=stub_persephone_service,
            jwt_service=stub_jwt_service
        )


def test_create_electronic_signature_jwt_failed_to_generate_session_and_fail_to_send_to_persephone(
    get_new_stub_persephone_service,
    get_new_stub_jwt_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_jwt_service = get_new_stub_jwt_service
    get_new_stub_jwt_service.generate_session_jwt = MagicMock(side_effect=Exception())
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        AuthenticationService.create_electronic_signature_jwt(
            change_electronic_signature_request={
                "electronic_signature": "",
                "email": "",
            },
            persephone_client=stub_persephone_service,
            jwt_service=stub_jwt_service
        )


def test_create_electronic_signature_jwt_sent_to_persephone(
    get_new_stub_persephone_service,
    get_new_stub_jwt_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_jwt_service = get_new_stub_jwt_service
    session_jwt = ('jwt_generated', True)
    get_new_stub_jwt_service.generate_session_jwt = MagicMock(return_value=session_jwt)
    stub_persephone_service.run = MagicMock(return_value=True)
    response = AuthenticationService.create_electronic_signature_jwt(
        change_electronic_signature_request={
                "electronic_signature": "",
                "email": "",
            },
        persephone_client=stub_persephone_service,
        jwt_service=stub_jwt_service
    )
    assert response['status_code'] == status.HTTP_200_OK
    assert response['payload'] == session_jwt[0]


def test_create_electronic_signature_jwt_fail_to_send_to_persephone(
    get_new_stub_persephone_service,
    get_new_stub_jwt_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_jwt_service = get_new_stub_jwt_service
    get_new_stub_jwt_service.generate_session_jwt = MagicMock(return_value=('jwt_generated', True))
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        AuthenticationService.create_electronic_signature_jwt(
            change_electronic_signature_request={
                "electronic_signature": "",
                "email": "",
            },
            persephone_client=stub_persephone_service,
            jwt_service=stub_jwt_service
        )


def test_logout(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    response = AuthenticationService.logout(
        device_jwt_and_thebes_answer_from_request={
            "jwt": "",
            "email": "",
            "device_information": {}
        },
        persephone_client=stub_persephone_service
    )
    assert response['status_code'] == status.HTTP_200_OK
    assert response['message_key'] == "email.logout"


def test_logout_fail_to_sent_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
         AuthenticationService.logout(
            device_jwt_and_thebes_answer_from_request={
                "jwt": "",
                "email": "",
                "device_information": {}
            },
            persephone_client=stub_persephone_service
        )
