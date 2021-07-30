# STANDARD LIBS
from copy import deepcopy
from fastapi import status

# SPHINX
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.user.repository import UserRepository
from src.exceptions.exceptions import BadRequestError
from src.services.persephone.service import PersephoneService
from src.utils.stone_age import StoneAge
from src.utils.base_model_normalizer import normalize_enum_types


class SinacorService:
    @staticmethod
    def process_callback(
        payload: dict,
        client_register_repository=ClientRegisterRepository(),
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ):
        successful = payload.get("successful")
        error = payload.get("error")
        if successful is False or error is not None:
            raise BadRequestError("bureau.error.fail")

        # Send to Persephone
        # table_result = persephone_client.run(
        #     topic="thebes.sphinx_persephone.topic",
        #     partition=5,
        #     payload=get_user_account_template_with_data(payload=payload),m
        #     schema_key="table_schema",
        # )
        # if table_result is False:
        #     raise InternalServerError("common.process_issue")

        # UPDATE user data
        stoneage_output = payload.get("output")
        old_user_data = user_repository.find_one({"_id": stoneage_output["email"]["value"]})
        new_user_data = SinacorService.merge_data_and_get_completed_user_data(
            output=stoneage_output, user_database_document=old_user_data
        )

        client_register_repository.cleanup_temp_tables(user_cpf=new_user_data["cpf"])
        sinacor_user_control_data = (
            client_register_repository.get_user_control_data_if_user_already_exists(
                user_cpf=new_user_data["cpf"]
            )
        )
        is_update = sinacor_user_control_data is not None
        builder = client_register_repository.get_builder(
            user_data=new_user_data, sinacor_user_control_data=sinacor_user_control_data
        )
        client_register_repository.register_user_data_in_register_users_temp_table(
            builder=builder
        )
        if is_update is False:
            has_error = client_register_repository.validate_user_data_erros(
                user_cpf=new_user_data["cpf"]
            )
            if has_error:
                raise BadRequestError("bureau.error.fail")
        client_register_repository.register_validated_users(user_cpf=new_user_data["cpf"])
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "ok",
        }

    @staticmethod
    def merge_data_and_get_completed_user_data(
        output: dict, user_database_document: dict
    ) -> dict:
        new = deepcopy(user_database_document)
        output_normalized = StoneAge.get_only_values_from_user_data(user_data=output)
        normalize_enum_types(output_normalized)
        new.update({"stone_age_decision": output_normalized["decision"]})
        del output_normalized["decision"]
        del output_normalized["status"]
        del output_normalized["email"]
        del output_normalized["date_of_acquisition"]
        new.update(output_normalized)
        return new
