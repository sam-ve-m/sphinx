# STANDARD LIBS
import datetime
import json
from copy import deepcopy
from fastapi import status

# SPHINX
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import PersephoneService
from src.utils.stone_age import StoneAge
from src.utils.base_model_normalizer import normalize_enum_types
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.solutiontech import Solutiontech


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
        dtvm_client_data_provided_by_bureau = payload.get("output")

        if successful is False or error is not None:
            raise BadRequestError("bureau.error.fail")

        user_by_cpf = user_repository.find_one({"cpf": dtvm_client_data_provided_by_bureau["cpf"]["value"]})
        if user_by_cpf is not None:
            raise BadRequestError("common.register_exists")

        user_database_document = user_repository.find_one(
            {"_id": dtvm_client_data_provided_by_bureau["email"]["value"]}
        )
        database_and_bureau_dtvm_client_data_merged = (
            SinacorService.merge_bureau_client_data_with_user_database(
                output=dtvm_client_data_provided_by_bureau,
                user_database_document=user_database_document,
            )
        )

        SinacorService.send_dtvm_client_data_to_persephone(
            persephone_client=persephone_client,
            dtvm_client_data=database_and_bureau_dtvm_client_data_merged,
        )

        sinacor_client_control_data = SinacorService.clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        SinacorService.insert_client_on_the_sinacor_temp_table(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            sinacor_client_control_data=sinacor_client_control_data,
        )

        SinacorService.check_sinacor_errors_if_is_not_update_client(
            client_register_repository=client_register_repository,
            sinacor_client_control_data=sinacor_client_control_data,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        client_register_repository.register_validated_users(
            user_cpf=database_and_bureau_dtvm_client_data_merged["cpf"]
        )

        database_and_bureau_dtvm_client_data_merged = SinacorService.add_dtvm_client_trade_metadata(
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
        )

        user_is_updated = user_repository.update_one(
            old=user_database_document,
            new=database_and_bureau_dtvm_client_data_merged,
        )

        if user_is_updated is False:
            raise InternalServerError("common.process_issue")

        bmf_account = database_and_bureau_dtvm_client_data_merged.get("bmf_account")
        Solutiontech.request_client_sync(user_bmf_code=int(bmf_account))

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "ok",
        }

    @staticmethod
    def send_dtvm_client_data_to_persephone(persephone_client, dtvm_client_data: dict):
        # Send to Persephone
        # table_result = persephone_client.run(
        #     topic="thebes.sphinx_persephone.topic",
        #     partition=5,
        #     payload=get_user_account_template_with_data(payload=dtvm_client_data),
        #     schema_key="table_schema",
        # )
        # if table_result is False:
        #     raise InternalServerError("common.process_issue")
        pass

    @staticmethod
    def clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
        client_register_repository: ClientRegisterRepository,
        database_and_bureau_dtvm_client_data_merged: dict,
    ):
        client_register_repository.cleanup_temp_tables(
            user_cpf=database_and_bureau_dtvm_client_data_merged["cpf"]
        )

        sinacor_user_control_data = (
            client_register_repository.get_user_control_data_if_user_already_exists(
                user_cpf=database_and_bureau_dtvm_client_data_merged["cpf"]
            )
        )

        return sinacor_user_control_data

    @staticmethod
    def require_sync_to_solutiontech_from_sinacor() -> str:
        return "send"

    @staticmethod
    def add_dtvm_client_trade_metadata(
        database_and_bureau_dtvm_client_data_merged: dict,
        client_register_repository: ClientRegisterRepository,
    ) -> dict:

        database_and_bureau_dtvm_client_data_merged.update(
            {"sinacor": True, "sincad": False}
        )
        sync_status = SinacorService.require_sync_to_solutiontech_from_sinacor()
        database_and_bureau_dtvm_client_data_merged.update(
            {"solutiontech": sync_status}
        )

        sinacor_user_control_data = (
            client_register_repository.get_user_control_data_if_user_already_exists(
                user_cpf=database_and_bureau_dtvm_client_data_merged["cpf"]
            )
        )

        account_prefix = sinacor_user_control_data[0]
        account_digit = sinacor_user_control_data[1]

        bovespa_account = SinacorService.build_bovespa_account_mask(
            account_prefix=account_prefix, account_digit=account_digit
        )
        bmf_account = SinacorService.build_bmf_account(account_prefix=account_prefix)

        database_and_bureau_dtvm_client_data_merged.update(
            {"bovespa_account": bovespa_account, "bmf_account": bmf_account}
        )

        database_and_bureau_dtvm_client_data_merged.update(
            {
                "last_modified_date": {"concluded_at": datetime.datetime.now()},
            }
        )

        return database_and_bureau_dtvm_client_data_merged

    @staticmethod
    def build_bovespa_account_mask(account_prefix: int, account_digit: int):
        number_of_account_prefix_digits = 9
        str_account_prefix = str(account_prefix)
        str_account_prefix_filled_with_zeros = str_account_prefix.zfill(
            number_of_account_prefix_digits
        )
        str_account_digit = str(account_digit)
        bovespa_account_mask = (
            f"{str_account_prefix_filled_with_zeros}-{str_account_digit}"
        )
        return bovespa_account_mask

    @staticmethod
    def build_bmf_account(account_prefix: int):
        bmf_account = str(account_prefix)
        return bmf_account

    @staticmethod
    def insert_client_on_the_sinacor_temp_table(
        client_register_repository: ClientRegisterRepository,
        database_and_bureau_dtvm_client_data_merged: dict,
        sinacor_client_control_data,
    ):
        builder = client_register_repository.get_builder(
            user_data=database_and_bureau_dtvm_client_data_merged,
            sinacor_user_control_data=sinacor_client_control_data,
        )

        client_register_repository.register_user_data_in_register_users_temp_table(
            builder=builder
        )

    @staticmethod
    def check_sinacor_errors_if_is_not_update_client(
        client_register_repository: ClientRegisterRepository,
        sinacor_client_control_data: dict,
        database_and_bureau_dtvm_client_data_merged: dict,
    ):
        is_update = sinacor_client_control_data is not None

        if is_update is False:
            has_error = client_register_repository.validate_user_data_erros(
                user_cpf=database_and_bureau_dtvm_client_data_merged["cpf"]
            )
            if has_error:
                raise BadRequestError("bureau.error.fail")

    @staticmethod
    def merge_bureau_client_data_with_user_database(
        output: dict, user_database_document: dict
    ) -> dict:
        new = deepcopy(user_database_document)
        output_normalized = StoneAge.get_only_values_from_user_data(user_data=output)
        normalize_enum_types(output_normalized)
        new.update({"register_analyses": output_normalized["decision"]})
        del output_normalized["decision"]
        del output_normalized["status"]
        del output_normalized["email"]
        del output_normalized["date_of_acquisition"]
        new.update(output_normalized)
        return new
