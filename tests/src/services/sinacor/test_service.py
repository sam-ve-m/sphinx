# Standards
from copy import deepcopy

# Third part
import pytest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError


# Sphinx
from src.services.sinacor.service import SinacorService
from tests.stub_classes.stub_persephone_service import StubPersephoneService
from src.exceptions.exceptions import InternalServerError, BadRequestError
from .fake_stone_age_response import fake_response
from .fake_user_data import fake_user
from .data_validator import (
    FirstLevelJsonUserMergedDataValidator,
    MinimalClientTradeMetadata,
)
from src.services.third_part_integration.solutiontech import Solutiontech
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus


class StubClientRegisterRepository:
    pass


@pytest.fixture
def get_new_stub_persephone_service():
    stub_persephone_service = StubPersephoneService()
    return stub_persephone_service


@pytest.fixture
def get_new_sinacor_service():
    sinacor_service = SinacorService()
    return sinacor_service


def test_send_dtvm_client_data_to_persephone_fail_to_sent(
    get_new_stub_persephone_service,
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SinacorService._send_dtvm_client_data_to_persephone(
            persephone_client=stub_persephone_service, dtvm_client_data={}
        )


def test_send_dtvm_client_data_to_persephone(get_new_stub_persephone_service):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=True)
    response = SinacorService._send_dtvm_client_data_to_persephone(
        persephone_client=stub_persephone_service, dtvm_client_data={}
    )
    assert response is None


def _validate_builder_response(callback, dict_to_validate: dict) -> bool:
    try:
        callback(**dict_to_validate)
        return True
    except ValidationError as ve:
        print(ve)
        return False


def test_merge_bureau_client_data_with_user_database_missing_keys_that_will_be_deleted():
    fake_response_obj = deepcopy(fake_response)
    fake_user_obj = deepcopy(fake_user)
    del fake_response_obj["data"]["decision"]
    del fake_response_obj["data"]["status"]
    del fake_response_obj["data"]["email"]
    del fake_response_obj["data"]["date_of_acquisition"]
    with pytest.raises(KeyError):
        SinacorService._merge_bureau_client_data_with_user_database(
            output=fake_response_obj["data"], user_database_document=fake_user_obj
        )


def test_merge_bureau_client_data_with_user_database():
    fake_response_obj = deepcopy(fake_response)
    fake_user_obj = deepcopy(fake_user)
    response = SinacorService._merge_bureau_client_data_with_user_database(
        output=fake_response_obj["data"], user_database_document=fake_user_obj
    )
    assert response.get("decision") is None
    assert response.get("status") is None
    assert response.get("date_of_acquisition") is None
    assert response.get("register_analyses") == fake_response_obj["data"]["decision"]
    assert _validate_builder_response(FirstLevelJsonUserMergedDataValidator, response)


def test_check_sinacor_errors_if_is_not_update_client_is_not_update():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.validate_user_data_erros = MagicMock(
        return_value=False
    )
    response = SinacorService._check_sinacor_errors_if_is_not_update_client(
        client_register_repository=stub_client_register_repository,
        sinacor_client_control_data=None,
        database_and_bureau_dtvm_client_data_merged={"cpf": 12345678900},
    )
    assert response is None


def test_check_sinacor_errors_if_is_not_update_client_is_not_update_and_fail():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.validate_user_data_erros = MagicMock(
        return_value=True
    )
    with pytest.raises(BadRequestError, match="bureau.error.fail"):
        SinacorService._check_sinacor_errors_if_is_not_update_client(
            client_register_repository=stub_client_register_repository,
            sinacor_client_control_data=None,
            database_and_bureau_dtvm_client_data_merged={"cpf": 12345678900},
        )


def test_check_sinacor_errors_if_is_not_update_client_is_update():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.validate_user_data_erros = MagicMock(
        return_value=False
    )
    response = SinacorService._check_sinacor_errors_if_is_not_update_client(
        client_register_repository=stub_client_register_repository,
        sinacor_client_control_data=(1,),
        database_and_bureau_dtvm_client_data_merged={"cpf": 12345678900},
    )
    assert response is None


def test_add_third_party_operator_information():
    user_data = {}
    SinacorService._add_third_party_operator_information(
        database_and_bureau_dtvm_client_data_merged=user_data
    )
    assert user_data.get("can_be_managed_by_third_party_operator") is not None
    assert user_data.get("is_managed_by_third_party_operator") is not None
    assert user_data.get("third_party_operator") is not None


def test_build_bovespa_account_mask_bovespa_account_to_long():
    with pytest.raises(InternalServerError, match="Bovespa account to lon"):
        SinacorService._build_bovespa_account_mask(
            account_prefix=11111111111, account_digit=1
        )


def test_build_bovespa_account_mask():
    bovespa_account_mask = SinacorService._build_bovespa_account_mask(
        account_prefix=1, account_digit=1
    )
    assert bovespa_account_mask == "000000001-1"


def test_build_bovespa_account_mask_exact_match():
    bovespa_account_mask = SinacorService._build_bovespa_account_mask(
        account_prefix=111111111, account_digit=1
    )
    assert bovespa_account_mask == "111111111-1"


def test_build_bmf_account_int_input():
    bmf_account = SinacorService._build_bmf_account(account_prefix=1)
    assert isinstance(bmf_account, str)
    assert bmf_account == "1"


def test_build_bmf_account_str_input():
    bmf_account = SinacorService._build_bmf_account(account_prefix="1")
    assert isinstance(bmf_account, str)
    assert bmf_account == "1"


@patch.object(Solutiontech, "request_client_sync", return_value=False)
def test_require_sync_to_solutiontech_from_sinacor_is_not_synced(mock):
    result = SinacorService._require_sync_to_solutiontech_from_sinacor(bmf_account=11)
    assert result == SolutiontechClientImportStatus.FAILED.value


@patch.object(Solutiontech, "request_client_sync", return_value=True)
def test_require_sync_to_solutiontech_from_sinacoris_synced(mock):
    result = SinacorService._require_sync_to_solutiontech_from_sinacor(bmf_account=11)
    assert result == SolutiontechClientImportStatus.SEND.value


@patch.object(Solutiontech, "request_client_sync", return_value=False)
def test_add_dtvm_client_trade_metadata_without_sincad(mock):
    database_and_bureau_dtvm_client_data_merged = {"cpf": "12345678900"}
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_user_control_data_if_user_already_exists = (
        MagicMock(return_value=(12, 2))
    )
    result = SinacorService._add_dtvm_client_trade_metadata(
        database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        client_register_repository=stub_client_register_repository,
    )
    assert _validate_builder_response(MinimalClientTradeMetadata, result)
    assert result["sincad"] is False


@patch.object(Solutiontech, "request_client_sync", return_value=False)
def test_add_dtvm_client_trade_metadata_with_sincad(mock):
    database_and_bureau_dtvm_client_data_merged = {"cpf": "12345678900", "sincad": True}
    stub_client_register_repository = StubClientRegisterRepository()
    stub_client_register_repository.get_user_control_data_if_user_already_exists = (
        MagicMock(return_value=(12, 2))
    )
    result = SinacorService._add_dtvm_client_trade_metadata(
        database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        client_register_repository=stub_client_register_repository,
    )
    assert _validate_builder_response(MinimalClientTradeMetadata, result)
    assert result["sincad"] is True


class StubUserRepository:
    pass


def test_save_or_update_client_data_error_on_save():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_user_repository = StubUserRepository()
    stub_user_repository.update_one = MagicMock(return_value=False)
    with patch.object(
        SinacorService, "_create_client_into_sinacor", return_value=None
    ) as mock_create_client_into_sinacor:
        with patch.object(
            SinacorService, "_add_third_party_operator_information", return_value=None
        ) as mock_add_third_party_operator_information:
            with patch.object(
                SinacorService,
                "_add_dtvm_client_trade_metadata",
                return_value={"email": "", "cpf": ""},
            ) as mock_add_dtvm_client_trade_metadata:
                with pytest.raises(InternalServerError, match="common.process_issue"):
                    SinacorService.save_or_update_client_data(
                        user_data={},
                        client_register_repository=stub_client_register_repository,
                        user_repository=stub_user_repository,
                    )


def test_save_or_update_client_data():
    stub_client_register_repository = StubClientRegisterRepository()
    stub_user_repository = StubUserRepository()
    stub_user_repository.update_one = MagicMock(return_value=True)
    with patch.object(
        SinacorService, "_create_client_into_sinacor", return_value=None
    ) as mock_create_client_into_sinacor:
        with patch.object(
            SinacorService, "_add_third_party_operator_information", return_value=None
        ) as mock_add_third_party_operator_information:
            with patch.object(
                SinacorService,
                "_add_dtvm_client_trade_metadata",
                return_value={"email": "", "cpf": ""},
            ) as mock_add_dtvm_client_trade_metadata:
                SinacorService.save_or_update_client_data(
                    user_data={},
                    client_register_repository=stub_client_register_repository,
                    user_repository=stub_user_repository,
                )


@patch.object(SinacorService, "_send_dtvm_client_data_to_persephone", return_value=None)
@patch.object(SinacorService, "_merge_bureau_client_data_with_user_database", return_value=None)
@patch.object(SinacorService, "save_or_update_client_data", return_value=None)
def test_process_callback_error_to_find_user(
    mock_send_dtvm_client_data_to_persephone,
    mock_merge_bureau_client_data_with_user_database,
    mock_save_or_update_client_data,
    get_new_stub_persephone_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    stub_client_register_repository = StubClientRegisterRepository()
    stub_user_repository = StubUserRepository()
    stub_user_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_exists"):
        SinacorService.process_callback(
            payload={"data": {"email": {"value": ""}}},
            client_register_repository=stub_client_register_repository,
            user_repository=stub_user_repository,
            persephone_client=stub_persephone_service
        )


@patch.object(SinacorService, "_send_dtvm_client_data_to_persephone", return_value=None)
@patch.object(SinacorService, "_merge_bureau_client_data_with_user_database", return_value=None)
@patch.object(SinacorService, "save_or_update_client_data", return_value=None)
def test_process_callback(
    mock_send_dtvm_client_data_to_persephone,
    mock_merge_bureau_client_data_with_user_database,
    mock_save_or_update_client_data,
    get_new_stub_persephone_service
):
    stub_persephone_service = get_new_stub_persephone_service
    stub_persephone_service.run = MagicMock(return_value=False)
    stub_client_register_repository = StubClientRegisterRepository()
    stub_user_repository = StubUserRepository()
    stub_user_repository.find_one = MagicMock(return_value={"email": ""})
    SinacorService.process_callback(
        payload={"data": {"email": {"value": ""}}},
        client_register_repository=stub_client_register_repository,
        user_repository=stub_user_repository,
        persephone_client=stub_persephone_service
    )