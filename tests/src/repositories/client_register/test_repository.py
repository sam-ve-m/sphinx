# Std imports
from copy import deepcopy

# External imports
import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock

# Src imports
from src.exceptions.exceptions import InternalServerError
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from tests.src.repositories.client_register.test_repository_arguments import (
    valid_client_data,
    sinacor_insert_client_control_data, marital_married, unemployed_occupation, invalid_client_data,
)
from tests.src.repositories.client_register.test_repository_builder_validator import ValidNotMarriedBusinessPerson, ValidMarriedBusinessPerson, ValidMarriedUnemployed, ValidNotMarriedUnemployed, ValidMarriedEmployed, ValidNotMarriedEmployed


def _validate_builder_response(callback, dict_to_validate: dict) -> bool:
    try:
        callback(dict_to_validate)
        return True
    except ValidationError as ve:
        print(ve)
        return False


def test_get_builder_with_married_business_person_expect_valid_builder_callback_to_insert_client_into_sinacor():
    copied_valid_client_data = deepcopy(valid_client_data)
    copied_valid_client_data.update({"marital": marital_married})

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=False)
    sinacor_types_repository.is_business_person = MagicMock(return_value=True)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_married_business_person = (
        lambda dict_to_validate: ValidMarriedBusinessPerson(
            **dict_to_validate
        )
    )
    is_valid_married_business_person = _validate_builder_response(
        callback=validate_married_business_person,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_married_business_person is True


def test_get_builder_with_not_married_business_person_expect_valid_builder_callback_to_insert_client_into_sinacor():
    copied_valid_client_data = deepcopy(valid_client_data)

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=False)
    sinacor_types_repository.is_business_person = MagicMock(return_value=True)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_not_married_business_person = (
        lambda dict_to_validate: ValidNotMarriedBusinessPerson(
            **dict_to_validate
        )
    )
    is_valid_not_married_business_person = _validate_builder_response(
        callback=validate_not_married_business_person,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_not_married_business_person is True


def test_get_builder_with_married_unemployed_expect_valid_builder_callback_to_insert_client_into_sicnacor():
    copied_valid_client_data = deepcopy(valid_client_data)
    copied_valid_client_data.update({"marital": marital_married})
    copied_valid_client_data.update({"occupation": unemployed_occupation})

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=True)
    sinacor_types_repository.is_business_person = MagicMock(return_value=False)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_married_unemployed_occupation = (
        lambda dict_to_validate: ValidMarriedUnemployed(
            **dict_to_validate
        )
    )
    is_valid_married_other_occupation = _validate_builder_response(
        callback=validate_married_unemployed_occupation,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_married_other_occupation is True


def test_get_builder_with_not_married_unemployed_expect_valid_builder_callback_to_insert_client_into_sicnacor():
    copied_valid_client_data = deepcopy(valid_client_data)
    copied_valid_client_data.update({"occupation": unemployed_occupation})

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=True)
    sinacor_types_repository.is_business_person = MagicMock(return_value=False)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_not_married_unemployed_occupation = (
        lambda dict_to_validate: ValidNotMarriedUnemployed(
            **dict_to_validate
        )
    )
    is_valid_not_married_unemployed_occupation = _validate_builder_response(
        callback=validate_not_married_unemployed_occupation,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_not_married_unemployed_occupation is True


def test_get_builder_with_married_employed_person_expect_valid_builder_callback_to_insert_client_into_sinacor():
    copied_valid_client_data = deepcopy(valid_client_data)
    copied_valid_client_data.update({"marital": marital_married})

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=False)
    sinacor_types_repository.is_business_person = MagicMock(return_value=True)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_married_employed = (
        lambda dict_to_validate: ValidMarriedEmployed(
            **dict_to_validate
        )
    )
    is_valid_married_employed_person = _validate_builder_response(
        callback=validate_married_employed,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_married_employed_person is True


def test_get_builder_with_not_married_employed_expect_valid_builder_callback_to_insert_client_into_sicnacor():
    copied_valid_client_data = deepcopy(valid_client_data)

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=True)
    sinacor_types_repository.is_business_person = MagicMock(return_value=False)

    builder = client_register_repository.get_builder(
        user_data=copied_valid_client_data,
        sinacor_user_control_data=sinacor_insert_client_control_data,
        sinacor_types_repository=sinacor_types_repository,
    )

    client_sinacor_dict = builder.build()

    validate_not_married_employed_occupation = (
        lambda dict_to_validate: ValidNotMarriedEmployed(
            **dict_to_validate
        )
    )
    is_valid_not_married_employed_occupation = _validate_builder_response(
        callback=validate_not_married_employed_occupation,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_not_married_employed_occupation is True


def test_get_builder_with_not_valid_occupation_data_expect_exception():
    copied_invalid_client_data = deepcopy(invalid_client_data)

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=True)
    sinacor_types_repository.is_business_person = MagicMock(return_value=False)

    with pytest.raises(KeyError, match="occupation"):

        builder = client_register_repository.get_builder(
            user_data=copied_invalid_client_data,
            sinacor_user_control_data=sinacor_insert_client_control_data,
            sinacor_types_repository=sinacor_types_repository,
        )


def test_get_builder_with_unemployed_and_business_person_data_expect_exception():
    copied_invalid_client_data = deepcopy(valid_client_data)

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_unemployed = MagicMock(return_value=True)
    sinacor_types_repository.is_business_person = MagicMock(return_value=True)

    with pytest.raises(InternalServerError, match="internal_error"):
        builder = client_register_repository.get_builder(
                user_data=copied_invalid_client_data,
                sinacor_user_control_data=sinacor_insert_client_control_data,
                sinacor_types_repository=sinacor_types_repository
        )
