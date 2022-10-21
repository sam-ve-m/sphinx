# Std imports
from copy import deepcopy
from unittest.mock import MagicMock

# External imports
import pytest
from pydantic import ValidationError

from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus

# Src imports
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator

# Test imports
from tests.src.services.builders.thebes_hall.test_thebes_hall_builder_arguments import (
    valid_client_data,
    ttl_10_seconds,
    valid_user_data,
    mocked_term,
)
from tests.src.services.builders.thebes_hall.test_thebes_hall_builder_validator import (
    ValidJwtPayloadToCompleteDtvmClient,
    ValidControlDataToCompleteDtvmClient,
    ValidJwtPayloadToCompleteAppUser,
    ValidControlDataToCompleteAppUser,
)


def _validate_builder_response(callback, dict_to_validate: dict) -> bool:
    try:
        callback(dict_to_validate)
        return True
    except ValidationError as ve:
        print(ve)
        return False


def test_builder_with_complete_dtvm_client_expect_valid_jwt_payload():
    copied_user_data = deepcopy(valid_client_data)

    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_risk_acknowledged = MagicMock(
        return_value="suitability"
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_user_data,
        ttl=ttl_10_seconds,
        user_repository=user_repository,
        terms_validator=terms_validator,
    )

    jwt_payload, control_data = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteDtvmClient(**dict_to_validate)
    )
    validate_control_data_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidControlDataToCompleteDtvmClient(
            **dict_to_validate
        )
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    is_valid_control_data = _validate_builder_response(
        callback=validate_control_data_to_complete_dtvm_user,
        dict_to_validate=control_data,
    )
    assert is_valid_jwt_payload is True
    assert is_valid_control_data is True
    assert jwt_payload["client_has_br_trade_allowed"] is True


def test_builder_with_empty_user_and_kwargs_expect_valid_recovery_exception():
    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_risk_acknowledged = MagicMock(
        return_value=None
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    with pytest.raises(Exception, match="internal_error"):
        thebes_hall_builder = ThebesHallBuilder(
            user_data={},
            ttl=ttl_10_seconds,
            user_repository=user_repository,
            terms_validator=terms_validator,
        )
        thebes_hall_builder.build()


def test_builder_with_complete_app_user_expect_valid_jwt_payload():
    copied_valid_user_data = deepcopy(valid_user_data)

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_valid_user_data,
        ttl=ttl_10_seconds,
        user_repository=UserRepository(),
        terms_validator=terms_validator,
    )

    jwt_payload, control_data = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteAppUser(**dict_to_validate)
    )
    validate_control_data_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidControlDataToCompleteAppUser(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    is_valid_control_data = _validate_builder_response(
        callback=validate_control_data_to_complete_dtvm_user,
        dict_to_validate=control_data,
    )
    assert is_valid_jwt_payload is True
    assert is_valid_control_data is True


class StubUserRepository:
    pass


def test_add_client_has_br_trade_allowed_solutiontech_length_0():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": "",
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_solutiontech_length_10():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": "1234567890",
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_solutiontech_failed():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.FAILED.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_solutiontech_send():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SEND.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_solutiontech_correct():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is True


def test_add_client_has_br_trade_allowed_suitability_lt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is True


def test_add_client_has_br_trade_allowed_suitability_gt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 25
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_suitability_eq():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 24
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_modified_date_lt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is True


def test_add_client_has_br_trade_allowed_modified_date_gt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 25

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False


def test_add_client_has_br_trade_allowed_modified_date_eq():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 24

    thebes_hall_builder.add_client_has_br_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past,
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_br_trade_allowed"] is False
