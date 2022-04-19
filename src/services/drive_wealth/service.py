import asyncio

from src.domain.drive_wealth.file_type import DriveWealthFileSide, DriveWealthFileType
from src.domain.drive_wealth.kyc_status import KycStatus
from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.protfolio.repository import PortfolioRepository
from src.services.builders.client_register.us.builder import (
    ClientUpdateRegisterBuilderUs,
)
from src.services.valhalla.service import ValhallaService
from src.transports.dw.transport import DWTransport
from src.infrastructures.env_config import config
from src.repositories.user.repository import UserRepository
from src.domain.sinacor.sinacor_identifier_document_types import (
    SinacorIdentifierDocumentTypes,
)
from src.exceptions.exceptions import InternalServerError
from src.domain.drive_wealth.account import (
    DriveWealthAccountType,
    DriveWealthAccountManagementType,
    DriveWealthAccountTradingType,
)


class DriveWealthService:

    dw_transport = DWTransport
    file_repository = FileRepository

    @classmethod
    async def registry_update_client(
        cls,
        user_data: dict,
        user_repository=UserRepository,
        social_network_service=ValhallaService,
        portfolio_repository=PortfolioRepository,
    ):
        user_dw_id = user_data["portfolios"]["default"].get("us", {}).get("dw_id")
        account_id = user_data["portfolios"]["default"].get("us", {}).get("dw_account")
        is_update = bool(user_dw_id)
        need_create_account = not bool(account_id)
        update_user = {}
        if is_update:
            await cls._update_user_and_get_id(
                user_data=user_data, user_dw_id=user_dw_id
            )
        else:
            user_dw_id = await cls._save_user_and_get_id(user_data=user_data)
            update_user.update(
                {
                    "portfolios.default.us.dw_id": user_dw_id,
                    "dw": KycStatus.KYC_PROCESSING.value,
                }
            )

        await cls._send_user_document(user_data=user_data, user_dw_id=user_dw_id)

        if need_create_account:
            account_id = await cls._create_user_account(user_dw_id=user_dw_id)
            update_user.update({"portfolios.default.us.dw_account": account_id})
            unique_id = user_data["unique_id"]
            await social_network_service.register_user_portfolio_us(
                unique_id=unique_id, dw_account=account_id, dw_id=user_dw_id
            )
            await portfolio_repository.save_unique_id_by_account(
                account=account_id, unique_id=unique_id
            )

        if update_user:
            was_updated = await user_repository.update_one(
                old={"unique_id": user_data["unique_id"]}, new=update_user
            )
            if was_updated is False:
                raise InternalServerError("common.process_issue")

    @classmethod
    async def validate_kyc_status(cls, user_dw_id: str) -> str:
        status, response = await cls.dw_transport.call_kyc_status_get(
            user_id=user_dw_id
        )
        # TODO PERSEPHONE LOG AKI
        if not status:
            raise InternalServerError("common.unable_to_process")
        kyc_status = response["kyc"]["status"]["name"]
        return kyc_status

    @classmethod
    async def _create_user_account(cls, user_dw_id: str):
        status, response = await cls.dw_transport.call_registry_account_post(
            user_id=user_dw_id,
            account_type=DriveWealthAccountType.LIVE,
            account_management_type=DriveWealthAccountManagementType.SELF,
            trading_type=DriveWealthAccountTradingType.MARGIN,
            ignore_buying_power=False,
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
            SinacorIdentifierDocumentTypes.CH.value: DriveWealthFileType.DRIVER_LICENSE,
        }
        user_unique_id = user_data["unique_id"]
        document_front = cls.file_repository.get_file_as_base_64(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        document_back = cls.file_repository.get_file_as_base_64(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        document_front_base_64, document_back_base_64 = await asyncio.gather(
            document_front, document_back
        )
        sinacor_document_type = user_data["identifier_document"]["document_data"][
            "type"
        ]
        document_type = sinacor_dw_document_map[sinacor_document_type]
        save_user_document_front = cls.dw_transport.call_save_user_document_file_post(
            user_id=user_dw_id,
            document_type=document_type,
            document=document_front_base_64,
            side=DriveWealthFileSide.FRONT,
        )
        save_user_document_back = cls.dw_transport.call_save_user_document_file_post(
            user_id=user_dw_id,
            document_type=document_type,
            document=document_back_base_64,
            side=DriveWealthFileSide.BACK,
        )
        (
            save_user_document_front_result,
            save_user_document_back_result,
        ) = await asyncio.gather(save_user_document_front, save_user_document_back)
        status_document_front = save_user_document_front_result[0]
        status_document_back = save_user_document_back_result[0]
        if not (status_document_front and status_document_back):
            raise InternalServerError("common.unable_to_process")

    @classmethod
    async def _save_user_and_get_id(cls, user_data: dict) -> str:
        builder = cls.__get_registry_body(user_data=user_data)
        registry_body = builder.build()
        status, response = await cls.dw_transport.call_registry_user_post(
            user_register_data=registry_body
        )
        # TODO PERSEPHONE LOG AKI
        if not status:
            raise InternalServerError("common.unable_to_process")
        user_id = response["id"]
        return user_id

    @classmethod
    async def _update_user_and_get_id(cls, user_data: dict, user_dw_id: str) -> str:
        builder = cls.__get_update_body(user_data=user_data)
        registry_body = builder.build()
        status, response = await cls.dw_transport.call_registry_user_patch(
            user_register_data=registry_body, user_dw_id=user_dw_id
        )
        # TODO PERSEPHONE LOG AKI
        if not status:
            raise InternalServerError("common.unable_to_process")

    @staticmethod
    def __get_registry_body(user_data: dict) -> ClientUpdateRegisterBuilderUs:
        client_register_builder_us = ClientUpdateRegisterBuilderUs()
        (
            client_register_builder_us.add_parent_ibid()
            .add_parent_wlp_id()
            .add_user_type()
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

    @staticmethod
    def __get_update_body(user_data: dict) -> ClientUpdateRegisterBuilderUs:
        client_update_builder_us = ClientUpdateRegisterBuilderUs()
        (
            client_update_builder_us.add_basic_information_first_name(
                user_data=user_data
            )
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
        return client_update_builder_us
