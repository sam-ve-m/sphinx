# Std imports
from copy import deepcopy

# External imports
import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock

# Src imports
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from tests.src.repositories.client_register.test_thebes_hall_arguments import (
    valid_client_data,
    sinacor_insert_client_control_data,
)
from tests.src.repositories.client_register.test_thebes_hall_builder_validator import ValidNotMarriedBusinessPerson


def _validate_builder_response(callback, dict_to_validate: dict) -> bool:
    try:
        callback(dict_to_validate)
        return True
    except ValidationError as ve:
        print(ve)
        return False


def test_builder_with_not_married_business_person_expect_valid_builder_callback_to_insert_client_into_sinacor():
    copied_valid_client_data = deepcopy(valid_client_data)

    client_register_repository = ClientRegisterRepository()
    sinacor_types_repository = SinaCorTypesRepository()
    sinacor_types_repository.is_others = MagicMock(return_value=False)
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
    is_valid_married_employed_not_business_person = _validate_builder_response(
        callback=validate_not_married_business_person,
        dict_to_validate=client_sinacor_dict,
    )
    assert is_valid_married_employed_not_business_person is True
