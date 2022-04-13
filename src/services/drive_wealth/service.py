import asyncio

from src.domain.drive_wealth.file_type import DriveWealthFileSide, DriveWealthFileType
from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.services.builders.client_register.us.builder import ClientRegisterBuilderUs
from src.transports.dw.transport import DWTransport
from src.infrastructures.env_config import config
from src.repositories.user.repository import UserRepository
from src.domain.sinacor.sinacor_identifier_document_types import SinacorIdentifierDocumentTypes
from src.exceptions.exceptions import InternalServerError
from src.domain.drive_wealth.account import (
    DriveWealthAccountType,
    DriveWealthAccountManagementType,
    DriveWealthAccountTradingType
)



class DriveWealthService:

    dw_transport = DWTransport
    file_repository = FileRepository

    @classmethod
    async def registry_client(
        cls,
        user_data: dict,
        user_repository=UserRepository,
    ):
        user_dw_id = user_data["external_exchange_requirements"]["us"].get("user_id")
        account_id = user_data["portfolios"]["default"].get("us", {}).get("dw_account")
        is_update = bool(user_dw_id)
        need_create_account = not bool(account_id)
        update_user = {}
        if is_update:
            pass
        else:
            user_dw_id = await cls._save_user_and_get_id(user_data=user_data)
            update_user.update({"external_exchange_requirements.us.user_id": user_dw_id})

        await cls._send_user_document(user_data=user_data, user_dw_id=user_dw_id)

        if need_create_account:
            account_id = await cls._create_user_account(user_dw_id=user_dw_id)
            update_user.update({"portfolios.default.us.dw_account": account_id})

        if update_user:
            was_updated = await user_repository.update_one(
                old={"unique_id": user_data["unique_id"]},
                new=update_user
            )
            if was_updated is False:
                raise InternalServerError("common.process_issue")

    @classmethod
    async def _create_user_account(cls, user_dw_id: str):
        status, response = await cls.dw_transport.call_registry_account_post(
            user_id=user_dw_id,
            account_type=DriveWealthAccountType.LIVE,
            account_management_type=DriveWealthAccountManagementType.SELF,
            trading_type=DriveWealthAccountTradingType.MARGIN,
            ignore_buying_power=False
        )
        # TODO PERSEPHONE LOG AKI
        if not status:
            raise InternalServerError("common.unable_to_process")
        user_id = response["accountNo"]
        return user_id

    @classmethod
    async def _send_user_document(cls, user_data: dict, user_dw_id: str) -> str:
        sinacor_dw_document_map = {
            SinacorIdentifierDocumentTypes.RG.value: DriveWealthFileType.NATIONAL_ID_CARD,
            SinacorIdentifierDocumentTypes.CH.value: DriveWealthFileType.DRIVER_LICENSE
        }
        user_unique_id = user_data["unique_id"]
        document_front = cls.file_repository.get_file_as_base_64(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES")
        )
        document_back = cls.file_repository.get_file_as_base_64(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES")
        )
        document_front_base_64, document_back_base_64 = await asyncio.gather(
            document_front,
            document_back
        )
        sinacor_document_type = user_data['identifier_document']['document_data']['type']
        document_type = sinacor_dw_document_map[sinacor_document_type]
        save_user_document_front = cls.dw_transport.call_save_user_document_file_post(
            user_id=user_dw_id,
            document_type=document_type,
            document=document_front_base_64,
            side=DriveWealthFileSide.FRONT
        )
        save_user_document_back = cls.dw_transport.call_save_user_document_file_post(
            user_id=user_dw_id,
            document_type=document_type,
            document=document_back_base_64,
            side=DriveWealthFileSide.BACK
        )
        save_user_document_front_result, save_user_document_back_result = await asyncio.gather(
            save_user_document_front,
            save_user_document_back
        )
        status_document_front = save_user_document_front_result[0]
        status_document_back = save_user_document_back_result[0]
        if not (status_document_front and status_document_back):
            raise InternalServerError("common.unable_to_process")

    @classmethod
    async def _save_user_and_get_id(cls, user_data: dict) -> str:
        builder = cls.__get_registry_body(user_data=user_data)
        registry_body = builder.build()
        status, response = await cls.dw_transport.call_registry_user_post(user_register_data=registry_body)
        # TODO PERSEPHONE LOG AKI
        if not status:
            raise InternalServerError("common.unable_to_process")
        user_id = response["id"]
        return user_id

    @staticmethod
    def __get_registry_body(user_data: dict) -> ClientRegisterBuilderUs:
        client_register_builder_us = ClientRegisterBuilderUs()
        (
            client_register_builder_us.add_parent_ibid(user_data=user_data)
            .add_basic_information_first_name(user_data=user_data)
            .add_basic_information_last_name(user_data=user_data)
            .add_basic_information_country(user_data=user_data)
            .add_basic_information_phone(user_data=user_data)
            .add_basic_information_email(user_data=user_data)
            .add_basic_information_language()
            .add_tax_id_information_number(user_data=user_data)
            .add_tax_id_information_type(user_data=user_data)
            .add_tax_id_information_citizenship(user_data=user_data)
            .add_tax_id_information_us_tax_payer(user_data=user_data)
            .add_tax_residence_information_tax_treaty_with_us(user_data=user_data)
            .add_personal_information_birth_date(user_data=user_data)
            .add_personal_information_gender(user_data=user_data)
            .add_personal_information_marital(user_data=user_data)
            .add_personal_information_politically_exposed_names(user_data=user_data)
            .add_personal_information_irs_backup_withholdings()
            .add_address_street1(user_data=user_data)
            .add_address_city(user_data=user_data)
            .add_address_province(user_data=user_data)
            .add_address_zip_code(user_data=user_data)
            .add_address_country(user_data=user_data)
            .add_employment_status(user_data=user_data)
            .add_employment_company(user_data=user_data)
            .add_employment_type(user_data=user_data)
            .add_employment_position(user_data=user_data)
            .add_employment_broker(user_data=user_data)
            .add_employment_director_of(user_data=user_data)
            .add_investing_profile_investment_experience(user_data=user_data)
            .add_investing_profile_investment_objectives()
            .add_investing_profile_annual_income(user_data=user_data)
            .add_investing_profile_networth(user_data=user_data)
            .add_investing_profile_risk_tolerance()
            .add_disclosures_customer_agreement(user_data=user_data)
            .add_disclosures_terms_of_use(user_data=user_data)
            .add_disclosures_data_sharing(user_data=user_data)
            .add_disclosures_privacy_policy(user_data=user_data)
            .add_disclosures_name(user_data=user_data)
            .add_disclosures_rule14b(user_data=user_data)
            .add_disclosures_defaults()
            .add_margin_disclosure_agreement()
        )
        return client_register_builder_us


if __name__ == "__main__":
    import datetime
    import asyncio
    user_data = {'pin': None, 'nick_name': 'RAST3', 'email': 'msa@lionx.com.br', 'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'created_at': datetime.datetime(2022, 1, 2, 5, 59, 22, 598000), 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'is_active_user': True, 'must_do_first_login': False, 'use_magic_link': True, 'token_valid_after': datetime.datetime(2022, 1, 2, 8, 59, 22, 598000), 'terms': {'term_application': None, 'term_open_account': None, 'term_retail_liquid_provider': None, 'term_refusal': {'version': 4, 'date': datetime.datetime(2022, 3, 28, 13, 17, 13, 165000), 'is_deprecated': False}, 'term_non_compliance': None, 'term_application_dw': {'version': 1, 'date': 1649724839.644754, 'is_deprecated': False}, 'term_data_sharing_policy_dw': {'version': 1, 'date': 1649724840.032064, 'is_deprecated': False}, 'term_open_account_dw': {'version': 1, 'date': 1649724839.351827, 'is_deprecated': False}, 'term_privacy_policy_dw': {'version': 1, 'date': 1649724839.775732, 'is_deprecated': False}}, 'suitability': {'score': 1, 'submission_date': datetime.datetime(2022, 1, 2, 6, 8, 13, 422000), 'suitability_version': 1, 'months_past': 3}, 'identifier_document': {'cpf': '53845387084', 'document_data': {'type': 'RG', 'number': '385722594', 'date': datetime.datetime(2019, 3, 17, 21, 0), 'issuer': 'SSP', 'state': 'SP'}}, 'phone': '11987450574', 'tax_residences': [{'country': 'BRA', 'tax_number': '1292-00'}], 'bureau_status': 'approved', 'client_type': 1, 'connected_person': 'N', 'cosif_tax_classification': 21, 'investor_type': 101, 'is_bureau_data_validated': True, 'marital': {'status': 1, 'spouse': None}, 'person_type': 'F', 'address': {'country': 'BRA', 'street_name': 'RUA IMBUIA', 'city': 5150, 'number': '153', 'zip_code': '06184110', 'neighborhood': 'CIDADE DAS FLORES', 'state': 'SP'}, 'birthplace': {'country': 'BRA', 'state': 'SP', 'city': 'OSASCO', 'id_city': 5150}, 'assets': {'patrimony': 200000, 'income_tax_type': 1, 'date': datetime.datetime(2022, 1, 2, 0, 0, 0, 213000), 'income': 200000}, 'birth_date': datetime.datetime(1993, 10, 9, 0, 0), 'cel_phone': '11952909942', 'father_name': 'Argemiro Ferreira de Almeida', 'gender': 'M', 'mother_name': 'Vanessa Sievers de Almeida', 'name': 'Marco Sievers de Almeida', 'nationality': 1, 'occupation': {'activity': 609, 'company': {'cnpj': '36923006000188', 'name': 'LionX'}}, 'can_be_managed_by_third_party_operator': False, 'is_active_client': True, 'is_managed_by_third_party_operator': False, 'last_modified_date': {'concluded_at': datetime.datetime(2022, 2, 3, 13, 36, 26, 306000), 'months_past': 2}, 'sinacor': True, 'sincad': True, 'solutiontech': 'sync', 'third_party_operator': {'is_third_party_operator': False, 'details': {}, 'third_party_operator_email': 'string'}, 'electronic_signature': 'ea73ced01f94d96f7f46682055d6e3915b626a2ebbf98818a09ea2efb6af1a9e', 'electronic_signature_wrong_attempts': 0, 'is_blocked_electronic_signature': False, 'portfolios': {'default': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {}}, 'vnc': {'br': [{'bovespa_account': '000000071-5', 'bmf_account': '71'}, {'bovespa_account': '000000018-9', 'bmf_account': '18'}]}}, 'is_admin': True, 'external_exchange_requirements': {'us': {'is_politically_exposed': False, 'is_exchange_member': False, 'is_company_director': False, 'is_company_director_of': None, 'time_experience': 'YRS_1_2'}}}
    asyncio.run(DriveWealthService.registry_client(user_data=user_data))
