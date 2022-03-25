# STANDARD LIBS
import datetime
from typing import Type
from copy import deepcopy

from fastapi import status
from nidavellir import Sindri

# SPHINX
from src.domain.sinacor.client_sinacor_status import SinacorClientStatus
from src.domain.sincad.client_sync_status import SincadClientImportStatus
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.user.repository import UserRepository
from persephone_client import Persephone
from src.services.third_part_integration.solutiontech import Solutiontech


class SinacorService:

    persephone_client = Persephone

    @staticmethod
    async def save_or_update_client_data(
        user_data: dict,
        client_register_repository=ClientRegisterRepository,
        user_repository=UserRepository,
    ):
        database_and_bureau_dtvm_client_data_merged = (
            await SinacorService._create_or_update_client_into_sinacor(
                client_register_repository=client_register_repository,
                database_and_bureau_dtvm_client_data_merged=user_data,
            )
        )

        SinacorService._add_third_party_operator_information(
            database_and_bureau_dtvm_client_data_merged
        )

        database_and_bureau_dtvm_client_data_merged = await SinacorService._add_dtvm_client_trade_metadata(
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
        )

        await SinacorService.__crete_reference_to_allow_cash_transfer(
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
        )

        await SinacorService.__crete_link_with_graphic_account(
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
        )

        user_is_updated = await user_repository.update_one(
            old={"unique_id": database_and_bureau_dtvm_client_data_merged["unique_id"]},
            new=database_and_bureau_dtvm_client_data_merged,
        )

        if user_is_updated is False:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def _add_third_party_operator_information(
        database_and_bureau_dtvm_client_data_merged: dict,
    ):
        database_and_bureau_dtvm_client_data_merged.update(
            {
                "can_be_managed_by_third_party_operator": False,
                "is_managed_by_third_party_operator": False,
                "third_party_operator": {
                    "is_third_party_operator": False,
                    "details": {},
                    "third_party_operator_email": "string",
                },
            }
        )

    @classmethod
    async def _create_or_update_client_into_sinacor(
        cls,
        client_register_repository: Type[ClientRegisterRepository],
        database_and_bureau_dtvm_client_data_merged: dict,
    ):

        sinacor_client_control_data = await cls._clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        await cls._insert_client_on_the_sinacor_temp_table(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            sinacor_client_control_data=sinacor_client_control_data,
        )

        await cls._check_sinacor_errors_if_is_not_update_client(
            client_register_repository=client_register_repository,
            sinacor_client_control_data=sinacor_client_control_data,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        cpf_client = database_and_bureau_dtvm_client_data_merged.get(
            "identifier_document"
        ).get("cpf")
        await client_register_repository.register_validated_users(user_cpf=cpf_client)

        return database_and_bureau_dtvm_client_data_merged

    @staticmethod
    def _send_dtvm_client_data_to_persephone(dtvm_client_data: dict):
        # TODO: REMOVE THIS IS FROM STONEAGE
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.KYC_TABLE_QUEUE.value,
        #     payload=dtvm_client_data,
        #     schema_key="user_bureau_callback_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")
        pass

    @staticmethod
    async def _clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
        client_register_repository: Type[ClientRegisterRepository],
        database_and_bureau_dtvm_client_data_merged: dict,
    ):
        await client_register_repository.cleanup_temp_tables(
            user_cpf=database_and_bureau_dtvm_client_data_merged["identifier_document"][
                "cpf"
            ]
        )

        sinacor_user_control_data = await client_register_repository.get_user_control_data_if_user_already_exists(
            user_cpf=database_and_bureau_dtvm_client_data_merged["identifier_document"][
                "cpf"
            ]
        )

        return sinacor_user_control_data

    @staticmethod
    async def _require_sync_to_solutiontech_from_sinacor(bmf_account: int) -> str:
        is_synced_with_solutiontech = await Solutiontech.request_client_sync(
            user_bmf_code=bmf_account
        )

        if is_synced_with_solutiontech:
            return SolutiontechClientImportStatus.SEND.value
        return SolutiontechClientImportStatus.FAILED.value

    @staticmethod
    async def __crete_reference_to_allow_cash_transfer(
        database_and_bureau_dtvm_client_data_merged: dict,
        client_register_repository: Type[ClientRegisterRepository],
    ):
        client_code = database_and_bureau_dtvm_client_data_merged["portfolios"][
            "default"
        ]["br"]["bmf_account"]
        is_already_allowed_cash_transfer = (
            await client_register_repository.client_has_already_allowed_cash_transfer(
                client_code=client_code
            )
        )
        if not is_already_allowed_cash_transfer:
            await client_register_repository.allow_cash_transfer(
                client_code=int(client_code)
            )

    @staticmethod
    async def __crete_link_with_graphic_account(
        database_and_bureau_dtvm_client_data_merged: dict,
        client_register_repository: Type[ClientRegisterRepository],
    ):
        cpf = database_and_bureau_dtvm_client_data_merged["identifier_document"]["cpf"]
        is_already_allowed_cash_transfer = await client_register_repository.client_has_already_link_with_graphic_account(
            cpf=cpf
        )
        if not is_already_allowed_cash_transfer:
            await client_register_repository.link_client_with_graphic_account(
                cpf=int(cpf)
            )

    @staticmethod
    async def _add_dtvm_client_trade_metadata(
        database_and_bureau_dtvm_client_data_merged: dict,
        client_register_repository: Type[ClientRegisterRepository],
    ) -> dict:

        client_cpf = database_and_bureau_dtvm_client_data_merged.get(
            "identifier_document"
        ).get("cpf")

        database_and_bureau_dtvm_client_data_merged.update(
            {"sinacor": SinacorClientStatus.CREATED.value}
        )

        if database_and_bureau_dtvm_client_data_merged.get("sincad") is None:
            database_and_bureau_dtvm_client_data_merged.update(
                {
                    "sincad": SincadClientImportStatus.NOT_SYNCED.value,
                }
            )

        sinacor_user_control_data = await client_register_repository.get_user_control_data_if_user_already_exists(
            user_cpf=client_cpf
        )

        account_prefix = sinacor_user_control_data[0]
        account_digit = sinacor_user_control_data[1]

        bovespa_account = await SinacorService._build_bovespa_account_mask(
            account_prefix=account_prefix, account_digit=account_digit
        )
        bmf_account = SinacorService._build_bmf_account(account_prefix=account_prefix)

        sync_status = await SinacorService._require_sync_to_solutiontech_from_sinacor(
            int(bmf_account)
        )

        database_and_bureau_dtvm_client_data_merged.update(
            {"solutiontech": sync_status}
        )
        database_and_bureau_dtvm_client_data_merged.update(
            {
                "portfolios": {
                    "default": {
                        "br": {
                            "bovespa_account": bovespa_account,
                            "bmf_account": bmf_account,
                        },
                    },
                    "vnc": {"br": []},
                }
            }
        )
        database_and_bureau_dtvm_client_data_merged.update(
            {
                "last_modified_date": {"concluded_at": datetime.datetime.utcnow()},
                "is_active_client": True,
            }
        )

        return database_and_bureau_dtvm_client_data_merged

    @staticmethod
    async def _build_bovespa_account_mask(account_prefix: int, account_digit: int):
        str_account_prefix = str(account_prefix)
        str_account_digit = str(account_digit)
        bovespa_account_mask_without_prefix = (
            f"{str_account_prefix}-{str_account_digit}"
        )
        if len(bovespa_account_mask_without_prefix) > 11:
            raise InternalServerError(
                f"Bovespa account to long '{bovespa_account_mask_without_prefix}'"
            )
        number_of_account_prefix_digits = 11
        bovespa_account_mask = bovespa_account_mask_without_prefix.zfill(
            number_of_account_prefix_digits
        )
        return bovespa_account_mask

    @staticmethod
    def _build_bmf_account(account_prefix: int):
        bmf_account = str(account_prefix)
        return bmf_account

    @staticmethod
    async def _insert_client_on_the_sinacor_temp_table(
        client_register_repository: Type[ClientRegisterRepository],
        database_and_bureau_dtvm_client_data_merged: dict,
        sinacor_client_control_data,
    ):
        builder = await client_register_repository.get_builder(
            user_data=database_and_bureau_dtvm_client_data_merged,
            sinacor_user_control_data=sinacor_client_control_data,
        )

        await client_register_repository.register_user_data_in_register_users_temp_table(
            builder=builder
        )

    @staticmethod
    async def _check_sinacor_errors_if_is_not_update_client(
        client_register_repository: Type[ClientRegisterRepository],
        sinacor_client_control_data: dict,
        database_and_bureau_dtvm_client_data_merged: dict,
    ):
        is_update = sinacor_client_control_data is not None

        if is_update is False:
            has_error = await client_register_repository.validate_user_data_errors(
                user_cpf=database_and_bureau_dtvm_client_data_merged[
                    "identifier_document"
                ]["cpf"]
            )
            if has_error:
                raise BadRequestError("bureau.error.fail")

    @staticmethod
    def _merge_bureau_client_data_with_user_database(
        output: dict, user_database_document: dict
    ) -> dict:
        new = deepcopy(user_database_document)
        output_normalized = dict()
        # TODO REMOVE STONEAGE
        # StoneAge.get_only_values_from_user_data(
        #     user_data=output, new_user_data=output_normalized
        # )
        Sindri.dict_to_primitive_types(output_normalized)
        # new.update({"register_analyses": output_normalized["decision"]})
        # del output_normalized["decision"]
        # del output_normalized["status"]
        # del output_normalized["email"]
        # del output_normalized["date_of_acquisition"]
        new.update(output_normalized)
        return new
