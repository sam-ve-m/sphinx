# STANDARD LIBS
import datetime
import logging

from copy import deepcopy
from fastapi import status

# SPHINX
from src.domain.sinacor.client_sinacor_status import SinacorClientStatus
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import PersephoneService
from src.services.third_part_integration.stone_age import StoneAge
from nidavellir.src.uru import Sindri
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.third_part_integration.solutiontech import Solutiontech
from src.domain.sincad.client_sync_status import SincadClientImportStatus
from src.domain.persephone_queue.persephone_queue import PersephoneQueue
from src.infrastructures.env_config import config


class SinacorService:
    @staticmethod
    def process_callback(
        payload: dict,
        client_register_repository=ClientRegisterRepository(),
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ):
        dtvm_client_data_provided_by_bureau = payload.get("data")

        user_database_document = user_repository.find_one(
            {"_id": dtvm_client_data_provided_by_bureau["email"]["value"]}
        )

        user_from_database_exists = user_database_document

        if user_from_database_exists is None:
            raise BadRequestError("common.register_exists")

        # fake_stone_age = SinacorService._get_fake_stone_age_callback(email=user_database_document.get("_id"), cpf=user_database_document.get("cpf"))
        # dtvm_client_data_provided_by_bureau = SinacorService._merge_fake_object_with_stone_age_data(fake_object=fake_stone_age.get("data"), stone_age_data=dtvm_client_data_provided_by_bureau)

        fake_identifier_document = SinacorService._get_fake_identifier_document()
        dtvm_client_data_provided_by_bureau = (
            SinacorService._fill_not_exists_data_identifier_document(
                fake_identifier_document=fake_identifier_document,
                stone_age_data=dtvm_client_data_provided_by_bureau,
            )
        )

        SinacorService._send_dtvm_client_data_to_persephone(
            persephone_client=persephone_client,
            dtvm_client_data=dtvm_client_data_provided_by_bureau,
            user_email=user_database_document.get("email"),
        )

        database_and_bureau_dtvm_client_data_merged = (
            SinacorService._merge_bureau_client_data_with_user_database(
                output=dtvm_client_data_provided_by_bureau,
                user_database_document=user_database_document,
            )
        )

        SinacorService.save_or_update_client_data(
            user_data=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
            user_repository=user_repository,
        )

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "ok",
        }

    @staticmethod
    def save_or_update_client_data(
        user_data: dict,
        client_register_repository=ClientRegisterRepository(),
        user_repository=UserRepository(),
    ):

        database_and_bureau_dtvm_client_data_merged = (
            SinacorService._create_client_into_sinacor(
                client_register_repository=client_register_repository,
                database_and_bureau_dtvm_client_data_merged=user_data,
            )
        )

        SinacorService._add_third_party_operator_information(database_and_bureau_dtvm_client_data_merged)

        database_and_bureau_dtvm_client_data_merged = SinacorService._add_dtvm_client_trade_metadata(
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            client_register_repository=client_register_repository,
        )

        user_is_updated = user_repository.update_one(
            old={"_id": database_and_bureau_dtvm_client_data_merged.get("email")},
            new=database_and_bureau_dtvm_client_data_merged,
        )

        if user_is_updated is False:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def _add_third_party_operator_information(
            database_and_bureau_dtvm_client_data_merged: dict,
    ) -> dict:
        database_and_bureau_dtvm_client_data_merged.update({
            "can_be_managed_by_third_party_operator": False,
            "is_managed_by_third_party_operator": False,
            "third_party_operator": {
                "is_third_party_operator": False,
                "details": {},
                "third_party_operator_email": "string",
            }
        })

    @staticmethod
    def _fill_not_exists_data_identifier_document(
        fake_identifier_document: dict, stone_age_data: dict
    ) -> dict:
        stone_age_identifier_document = (
            stone_age_data.get("identifier_document")
            if stone_age_data.get("identifier_document") is not None
            else {}
        )
        message = f"stone_age_data: {stone_age_identifier_document} - fake_identifier_document: {fake_identifier_document}"
        logging.info(msg=message)

        fake_object_keys = fake_identifier_document.keys()
        for fake_object_key in fake_object_keys:
            message = f"root-key: {fake_object_key}"
            logging.info(msg=message)
            stone_age_identifier_document[fake_object_key] = SinacorService.chupeta(
                fake_object=fake_identifier_document.get(fake_object_key),
                stone_age_data=stone_age_identifier_document.get(fake_object_key),
            )

        stone_age_data.update({"identifier_document": stone_age_identifier_document})
        return stone_age_data

    @staticmethod
    def chupeta(fake_object: dict, stone_age_data: dict):
        if stone_age_data is None:
            logging.info(msg=fake_object)
            stone_age_data = fake_object
        elif type(fake_object) is dict:
            inside_keys = fake_object.keys()
            for inside_key in inside_keys:
                logging.info(msg=inside_key)
                updated_value = SinacorService.chupeta(
                    fake_object=fake_object.get(inside_key),
                    stone_age_data=stone_age_data.get(inside_key),
                )
                stone_age_data[inside_key] = updated_value
        else:
            if stone_age_data is None:
                logging.info(msg=fake_object)
                stone_age_data = fake_object

        return stone_age_data

    # @staticmethod
    # def _merge_fake_object_with_stone_age_data(fake_object: dict, stone_age_data: dict) -> dict:
    #     message = f"stone_age_data: {stone_age_data} - fake_object: {fake_object}"
    #     logging.info(msg=message)
    #     fake_object_keys = fake_object.keys()
    #     for fake_object_key in fake_object_keys:
    #         message = f"root-key: {fake_object_key}"
    #         logging.info(msg=message)
    #         stone_age_data[fake_object_key] = SinacorService.chupeta(fake_object=fake_object.get(fake_object_key), stone_age_data=stone_age_data.get(fake_object_key))
    #
    #     return stone_age_data

    @staticmethod
    def _create_client_into_sinacor(
        client_register_repository: ClientRegisterRepository,
        database_and_bureau_dtvm_client_data_merged: dict,
    ):

        sinacor_client_control_data = SinacorService._clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        SinacorService._insert_client_on_the_sinacor_temp_table(
            client_register_repository=client_register_repository,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
            sinacor_client_control_data=sinacor_client_control_data,
        )

        SinacorService._check_sinacor_errors_if_is_not_update_client(
            client_register_repository=client_register_repository,
            sinacor_client_control_data=sinacor_client_control_data,
            database_and_bureau_dtvm_client_data_merged=database_and_bureau_dtvm_client_data_merged,
        )

        cpf_client = database_and_bureau_dtvm_client_data_merged.get("cpf")
        client_register_repository.register_validated_users(user_cpf=cpf_client)

        return database_and_bureau_dtvm_client_data_merged

    @staticmethod
    def _send_dtvm_client_data_to_persephone(
        persephone_client, dtvm_client_data: dict, user_email: str
    ):
        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.KYC_TABLE_QUEUE.value,
            payload=dtvm_client_data,
            schema_key="user_bureau_callback_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def _clean_sinacor_temp_tables_and_get_client_control_data_if_already_exists(
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
    def _require_sync_to_solutiontech_from_sinacor(bmf_account: int) -> str:
        is_synced_with_solutiontech = Solutiontech.request_client_sync(
            user_bmf_code=bmf_account
        )

        if is_synced_with_solutiontech:
            return SolutiontechClientImportStatus.SEND.value
        return SolutiontechClientImportStatus.FAILED.value

    @staticmethod
    def _add_dtvm_client_trade_metadata(
        database_and_bureau_dtvm_client_data_merged: dict,
        client_register_repository: ClientRegisterRepository,
    ) -> dict:

        client_cpf = database_and_bureau_dtvm_client_data_merged.get("cpf")

        database_and_bureau_dtvm_client_data_merged.update(
            {"sinacor": SinacorClientStatus.CREATED.value}
        )

        if database_and_bureau_dtvm_client_data_merged.get("sincad") is None:
            database_and_bureau_dtvm_client_data_merged.update(
                {
                    "sincad": SincadClientImportStatus.NOT_SYNCED.value,
                }
            )

        sinacor_user_control_data = (
            client_register_repository.get_user_control_data_if_user_already_exists(
                user_cpf=client_cpf
            )
        )

        account_prefix = sinacor_user_control_data[0]
        account_digit = sinacor_user_control_data[1]

        bovespa_account = SinacorService._build_bovespa_account_mask(
            account_prefix=account_prefix, account_digit=account_digit
        )
        bmf_account = SinacorService._build_bmf_account(account_prefix=account_prefix)

        sync_status = SinacorService._require_sync_to_solutiontech_from_sinacor(
            int(bmf_account)
        )

        database_and_bureau_dtvm_client_data_merged.update(
            {"solutiontech": sync_status}
        )
        database_and_bureau_dtvm_client_data_merged.update(
            {"bovespa_account": bovespa_account, "bmf_account": bmf_account}
        )
        database_and_bureau_dtvm_client_data_merged.update(
            {
                "last_modified_date": {"concluded_at": datetime.datetime.now()},
                "is_active_client": True,
            }
        )

        return database_and_bureau_dtvm_client_data_merged

    @staticmethod
    def _build_bovespa_account_mask(account_prefix: int, account_digit: int):
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
    def _build_bmf_account(account_prefix: int):
        bmf_account = str(account_prefix)
        return bmf_account

    @staticmethod
    def _insert_client_on_the_sinacor_temp_table(
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
    def _check_sinacor_errors_if_is_not_update_client(
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
    def _merge_bureau_client_data_with_user_database(
        output: dict, user_database_document: dict
    ) -> dict:
        new = deepcopy(user_database_document)
        output_normalized = StoneAge.get_only_values_from_user_data(user_data=output)
        Sindri.dict_to_primitive_types(output_normalized)
        new.update({"register_analyses": output_normalized["decision"]})
        del output_normalized["decision"]
        del output_normalized["status"]
        del output_normalized["email"]
        del output_normalized["date_of_acquisition"]
        new.update(output_normalized)
        return new

    @staticmethod
    def _get_fake_stone_age_callback(email: str, cpf: str):

        fake_response = {
            "proposal_id": "21b00324-d240-4c61-a79c-9a0bd7ff6e45",
            "data": {
                "status": "OK",
                "decision": "APROVADO",
                "gender": {"source": "PH3W", "value": "M"},
                "email": {"source": "PH3W", "value": email},
                "name": {"source": "PH3W", "value": "Antonio Armando Piaui"},
                "birth_date": {
                    "source": "PH3W",
                    "value": datetime.datetime(1993, 7, 12, 0, 0),
                },
                "birthplace": {
                    "nationality": {"source": "PH3W", "value": 1},
                    "country": {"source": "PH3W", "value": "BRA"},
                    "state": {"source": "PH3W", "value": "GO"},
                    "city": {"source": "PH3W", "value": "FORMOSA"},
                    "id_city": {"source": "PH3W", "value": 968},
                },
                "mother_name": {"source": "PH3W", "value": "Antonia dos Santos Jr."},
                "identifier_document": {
                    "type": {"source": "PH3W", "value": "RG"},
                    "document_data": {
                        # GENERATE
                        "number": {
                            "source": "PH3W",
                            "value": int(
                                "37.059.072-7".replace(".", "").replace("-", "")
                            ),
                        },
                        "date": {
                            "source": "PH3W",
                            "value": datetime.datetime(2018, 7, 12, 16, 31, 31),
                        },
                        "state": {"source": "PH3W", "value": "SP"},
                        "issuer": {"source": "PH3W", "value": "SSP"},
                    },
                },
                "address": {
                    "country": {"source": "PH3W", "value": "BRA"},
                    "street_name": {"source": "PH3W", "value": "R. 2"},
                    "number": {"source": "PH3W", "value": "126"},
                    "neighborhood": {"source": "PH3W", "value": "Formosinha"},
                    "state": {"source": "PH3W", "value": "GO"},
                    "city": {"source": "PH3W", "value": "FORMOSA"},
                    "id_city": {"source": "PH3W", "value": 968},
                    "zip_code": {"source": "PH3W", "value": 73813190},
                    "phone_number": {"source": "PH3W", "value": "11952909954"},
                },
                "occupation": {
                    "activity": {"source": "PH3W", "value": 304},
                    "company": {
                        "cnpj": {"source": "PH3W", "value": "25811052000179"},
                        "name": {"source": "PH3W", "value": "Tudo nosso .com.br"},
                    },
                },
                "assets": {
                    "patrimony": {"source": "PH3W", "value": 5446456.44},
                    "income": {"source": "PH3W", "value": 5446456.44},
                    "income_tax_type": {"source": "PH3W", "value": 1},
                    "date": {
                        "source": "PH3W",
                        "value": datetime.datetime(1993, 7, 12, 0, 0),
                    },
                },
                "education": {
                    "level": {"source": "PH3W", "value": "Médio incompleto"},
                    "course": {"source": "PH3W", "value": "Escola James Riwbon"},
                },
                "politically_exposed_person": {
                    "is_politically_exposed_person": {"source": "PH3W", "value": False}
                },
                "date_of_acquisition": {
                    "source": "PH3W",
                    "value": datetime.datetime(2018, 7, 12, 16, 31, 31),
                },
                "connected_person": {"source": "PH3W", "value": "N"},
                "person_type": {"source": "PH3W", "value": "F"},
                "client_type": {"source": "PH3W", "value": 1},
                "investor_type": {"source": "PH3W", "value": 101},
                "cosif_tax_classification": {"source": "PH3W", "value": 21},
                "marital": {
                    "status": {"source": "PH3W", "value": 5},
                    "spouse": {
                        "cpf": {"value": "16746756076", "source": "REQUEST"},
                        "name": {
                            "value": "Flavio Antobio Felicio",
                            "source": "REQUEST",
                        },
                        "nationality": {"value": 1, "source": "REQUEST"},
                    },
                },
                "cpf": {"source": "PH3W", "value": cpf},
                "self_link": {"source": "PH3W", "value": "http://self_user.jpg"},
                "is_us_person": {"source": "PH3W", "value": True},
                "us_tin": {"source": "PH3W", "value": 126516515},
                "irs_sharing": {"source": "PH3W", "value": True},
                "father_name": {"source": "PH3W", "value": "Antonio dos Santos"},
                "midia_person": {"source": "PH3W", "value": False},
                "person_related_to_market_influencer": {
                    "source": "PH3W",
                    "value": False,
                },
                "court_orders": {"source": "PH3W", "value": False},
                "lawsuits": {"source": "PH3W", "value": False},
                "fund_admin_registration": {"source": "PH3W", "value": False},
                "investment_fund_administrators_registration": {
                    "source": "PH3W",
                    "value": False,
                },
                "register_auditors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_of_other_market_participants_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "foreign_investors_register_of_annex_iv_not_registered": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_of_foreign_investors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_representative_of_nonresident_investors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
            },
        }

        return fake_response

    @staticmethod
    def _get_fake_identifier_document():
        fake_identifier_document = {
            "type": {"source": "LIONX", "value": "RG"},
            "document_data": {
                # GENERATE
                "number": {
                    "source": "LIONX",
                    "value": int("37.059.072-7".replace(".", "").replace("-", "")),
                },
                "date": {
                    "source": "LIONX",
                    "value": datetime.datetime(2018, 7, 12, 16, 31, 31),
                },
                "state": {"source": "LIONX", "value": "SP"},
                "issuer": {"source": "LIONX", "value": "SSP"},
            },
        }

        return fake_identifier_document
