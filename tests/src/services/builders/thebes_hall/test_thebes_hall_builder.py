# Std imports
from copy import deepcopy

# External imports
import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock

# Src imports
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus

# Test imports
from tests.src.services.builders.thebes_hall.test_thebes_hall_builder_arguments import (
    valid_client_data,
    kwargs_to_add_on_jwt,
    ttl_10_seconds,
    valid_user_data,
    not_active_user_data,
    mocked_term,
)
from tests.src.services.builders.thebes_hall.test_thebes_hall_builder_validator import (
    ValidJwtPayloadToCompleteDtvmClient,
    ForgotPasswordJwtPayload,
    ForgotElectronicSignatureJwtPayload,
    ValidJwtPayloadToCompleteAppUser,
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
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)

    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_refuse_term = MagicMock(
        return_value="suitability"
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=user_repository,
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteDtvmClient(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    assert is_valid_jwt_payload is True
    assert jwt_payload["client_has_trade_allowed"] is True


def test_builder_with_forgot_electronic_signature_expect_valid_recovery_jwt():
    copied_user_data = deepcopy(valid_client_data)
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)
    copied_kwargs_to_add_on_jwt.update({"forgot_electronic_signature": True})

    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_refuse_term = MagicMock(
        return_value="suitability"
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=user_repository,
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ForgotElectronicSignatureJwtPayload(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )

    assert is_valid_jwt_payload is True


def test_builder_with_forgot_password_expect_valid_recovery_jwt():
    copied_user_data = deepcopy(valid_client_data)
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)
    copied_kwargs_to_add_on_jwt.update({"forgot_password": True})

    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_refuse_term = MagicMock(
        return_value="suitability"
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=user_repository,
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ForgotPasswordJwtPayload(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )

    assert is_valid_jwt_payload is True


def test_builder_with_empty_user_and_kwargs_expect_valid_recovery_exception():
    user_repository = UserRepository()
    user_repository.is_user_using_suitability_or_refuse_term = MagicMock(
        return_value=None
    )

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    with pytest.raises(Exception, match="internal_error"):
        thebes_hall_builder = ThebesHallBuilder(
            user_data={},
            kwargs_to_add_on_jwt={},
            ttl=ttl_10_seconds,
            user_repository=user_repository,
            terms_validator=terms_validator,
        )
        thebes_hall_builder.build()


def test_builder_with_complete_app_user_expect_valid_jwt_payload():
    copied_valid_user_data = deepcopy(valid_user_data)
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_valid_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=UserRepository(),
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteAppUser(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    assert is_valid_jwt_payload is True


def test_builder_with_not_active_app_user_expect_valid_jwt_payload():
    copied_not_active_user_data = deepcopy(not_active_user_data)
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_not_active_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=UserRepository(),
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteAppUser(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    assert is_valid_jwt_payload is True


def test_builder_with_not_active_dtvm_client_expect_valid_jwt_payload():
    copied_valid_user_data = deepcopy(valid_user_data)
    copied_kwargs_to_add_on_jwt = deepcopy(kwargs_to_add_on_jwt)
    copied_valid_user_data.update({"is_active_user": False})

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data=copied_valid_user_data,
        kwargs_to_add_on_jwt=copied_kwargs_to_add_on_jwt,
        ttl=ttl_10_seconds,
        user_repository=UserRepository(),
        terms_validator=terms_validator,
    )

    jwt_payload = thebes_hall_builder.build()
    validate_jwt_payload_to_complete_dtvm_user = (
        lambda dict_to_validate: ValidJwtPayloadToCompleteAppUser(**dict_to_validate)
    )
    is_valid_jwt_payload = _validate_builder_response(
        callback=validate_jwt_payload_to_complete_dtvm_user,
        dict_to_validate=jwt_payload,
    )
    assert is_valid_jwt_payload is True


class StubUserRepository:
    pass


def test_add_client_has_trade_allowed_solutiontech_length_0():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": "",
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_solutiontech_length_10():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": "1234567890",
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_solutiontech_failed():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.FAILED.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_solutiontech_send():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SEND.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_solutiontech_correct():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is True


def test_add_client_has_trade_allowed_suitability_lt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is True


def test_add_client_has_trade_allowed_suitability_gt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 25
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_suitability_eq():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 24
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_modified_date_lt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 0

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is True


def test_add_client_has_trade_allowed_modified_date_gt():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 25

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False


def test_add_client_has_trade_allowed_modified_date_eq():

    terms_validator = TermsValidator()
    terms_validator.run = MagicMock(return_value=mocked_term)

    thebes_hall_builder = ThebesHallBuilder(
        user_data={
            "solutiontech": SolutiontechClientImportStatus.SYNC.value,
            "sincad": True,
            "sinacor": True,
            "is_active_client": True,
        },
        kwargs_to_add_on_jwt={},
        ttl=ttl_10_seconds,
        user_repository=StubUserRepository,
        terms_validator=terms_validator,
    )
    suitability_months_past = 0
    last_modified_date_months_past = 24

    thebes_hall_builder.add_client_has_trade_allowed(
        suitability_months_past=suitability_months_past,
        last_modified_date_months_past=last_modified_date_months_past
    )

    assert thebes_hall_builder._jwt_payload_data["client_has_trade_allowed"] is False
