import asyncio

from fastapi import status
from persephone_client import Persephone

from src.core.interfaces.services.authentication.interface import IAuthentication
from src.domain.drive_wealth.kyc_status import KycStatus
from src.domain.email.templates.enum import EmailTemplate
from src.domain.persephone_queue.persephone_queue import PersephoneQueue
from src.domain.sincad.client_sync_status import SincadClientImportStatus
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.domain.user_level.enum import UserLevel
from src.domain.validators.authenticate_validators import Cpf
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.infrastructures.env_config import config
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.cpf.repository import AllowedCpf
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
from src.services.drive_wealth.service import DriveWealthService
from src.services.email_builder.email import HtmlModifier
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.services.jwts.service import JwtService
from src.services.persephone.templates.persephone_templates import (
    get_user_thebes_hall_schema_template_with_data,
    get_create_electronic_signature_session_schema_template_with_data,
    get_user_logout_template_with_data,
    get_user_authentication_template_with_data,
)
from src.services.third_part_integration.solutiontech import Solutiontech


class AuthenticationService(IAuthentication):

    persephone_client = Persephone

    @staticmethod
    async def thebes_gate(
        thebes_answer: dict, user_repository=UserRepository, token_service=JwtService
    ) -> dict:
        user_data = await user_repository.find_one(
            {"unique_id": thebes_answer["user"].get("unique_id")}
        )
        if user_data is None:
            raise BadRequestError("common.register_not_exists")

        email_validated = user_data.get("email_validated")
        response = {"status_code": status.HTTP_200_OK, "payload": {"jwt": None}}
        is_email_validation_token = thebes_answer.get(
            "is_email_validation_token", False
        )
        if not email_validated and is_email_validation_token:
            update_data = {
                "is_active_user": True,
                "email_validated": True,
                "scope": {
                    "user_level": UserLevel.PROSPECT.value,
                    "view_type": "default",
                    "features": ["default"],
                },
            }
            if (
                await user_repository.update_one(old=user_data, new=update_data)
                is False
            ):
                raise InternalServerError("common.process_issue")
            user_data.update(update_data)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await AuthenticationService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
            partition=PersephoneQueue.USER_AUTHENTICATION.value,
            message=get_user_authentication_template_with_data(payload=user_data),
            schema_name="user_authentication_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()

        if is_third_party_token := thebes_answer.get("is_third_party_token"):
            jwt_payload_data.update({"is_third_party_token": is_third_party_token})

        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)

        response.update({"payload": {"jwt": jwt, "control_data": control_data}})

        return response

    @staticmethod
    async def validate_cpf(cpf: str, allowed_cpf=AllowedCpf) -> dict:
        try:
            cpf_validated = Cpf(cpf=cpf)
            is_allowed = await allowed_cpf.is_cpf_allowed(cpf=cpf_validated.cpf)
            response = {
                "status_code": status.HTTP_200_OK,
                "payload": {"is_allowed": is_allowed},
            }
            return response
        except Exception as e:
            raise BadRequestError("common.invalid_params")

    @staticmethod
    async def login(
        user_credentials: dict,
        user_repository=UserRepository(),
        token_service=JwtService,
    ) -> dict:
        user_data = await user_repository.find_one(
            {"email": user_credentials["email"].lower()}
        )
        if user_data is None:
            raise BadRequestError("common.register_not_exists")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=10
        ).build()

        is_active_user = user_data["is_active_user"]
        email_validated = user_data.get("email_validated", False)
        if email_validated and is_active_user is False:
            raise UnauthorizedError("invalid_credential")
        if not email_validated:
            jwt_payload_data.update({"is_email_validation_token": True})

        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)
        AuthenticationService.send_authentication_email(
            email_template=EmailTemplate.LOGIN,
            email=user_data["email"],
            payload_jwt=jwt,
            user_name=user_data["nick_name"],
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.login",
        }

    @staticmethod
    def send_authentication_email(
        email_template: EmailTemplate,
        email: str,
        payload_jwt: str,
        user_name: str,
        email_sender=SendGridEmail,
        origin: str = None,
    ) -> None:
        base_link = config("TARGET_LINK")
        if origin is not None:
            if origin == "picpay":
                base_link = config("TARGET_LINK_PICPAY")

        page = HtmlModifier(
            email_template=email_template,
            content={
                "cta": base_link + f"token={payload_jwt}",
                "nome": user_name,
            },
        )()
        email_sender.send_email_to(
            target_email=email,
            message=page,
            subject=i18n.get_translate(
                key=f"email.subject.{email_template.value}", locale="pt"
            ),
        )

    @staticmethod
    async def thebes_nock(data: dict) -> dict:
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"status": True},
        }

    @staticmethod
    async def thebes_hall(
        device_and_thebes_answer_from_request: dict,
        user_repository=UserRepository,
        token_service=JwtService,
    ) -> dict:
        x_thebes_answer = device_and_thebes_answer_from_request["x-thebes-answer"]
        unique_id = x_thebes_answer["user"]["unique_id"]
        user_data = await user_repository.find_one({"unique_id": unique_id})
        if user_data is None:
            raise BadRequestError("common.register_not_exists")

        user_data_update = {}
        must_update = False

        br_third_part_synchronization_status_task = (
            AuthenticationService._dtvm_client_has_br_trade_allowed(user=user_data)
        )

        us_third_part_synchronization_status_task = (
            AuthenticationService._dtvm_client_has_us_trade_allowed(user=user_data)
        )

        (
            br_third_part_synchronization_status,
            us_third_part_synchronization_status,
        ) = await asyncio.gather(
            br_third_part_synchronization_status_task,
            us_third_part_synchronization_status_task,
        )

        for key, value in br_third_part_synchronization_status.items():
            if value["status_changed"]:
                must_update = True
                user_data_update.update({key: value["status"]})

        for key, value in us_third_part_synchronization_status.items():
            if value["status_changed"]:
                must_update = True
                user_data_update.update({key: value["status"]})

        if must_update:
            if (
                await user_repository.update_one(old=user_data, new=user_data_update)
                is False
            ):
                raise InternalServerError("common.process_issue")
            user_data.update(user_data_update)

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()

        if is_third_party_token := x_thebes_answer.get("is_third_party_token"):
            jwt_payload_data.update({"is_third_party_token": is_third_party_token})

        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)
        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await AuthenticationService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
            partition=PersephoneQueue.USER_THEBES_HALL.value,
            message=get_user_thebes_hall_schema_template_with_data(
                unique_id=unique_id,
                jwt=jwt,
                jwt_payload_data=jwt_payload_data,
                device_information=device_and_thebes_answer_from_request.get(
                    "device_information"
                ),
            ),
            schema_name="user_thebes_hall_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"jwt": jwt, "control_data": control_data},
        }

    @staticmethod
    async def create_electronic_signature_jwt(
        change_electronic_signature_request: dict,
        jwt_service=JwtService,
    ):
        jwt_mist_session = None
        allowed = None
        try:
            jwt_mist_session = await jwt_service.generate_session_jwt(
                change_electronic_signature_request["electronic_signature"],
                change_electronic_signature_request["jwt_user"]["unique_id"],
            )
            allowed = True
        except BaseException as e:
            allowed = False
            raise e
        finally:
            sent_to_persephone = await AuthenticationService.persephone_client.send_to_persephone(
                topic=config("PERSEPHONE_TOPIC_USER"),
                partition=PersephoneQueue.USER_ELECTRONIC_SIGNATURE_SESSION.value,
                message=get_create_electronic_signature_session_schema_template_with_data(
                    unique_id=change_electronic_signature_request["jwt_user"][
                        "unique_id"
                    ],
                    mist_session=jwt_mist_session,
                    allowed=allowed,
                ),
                schema_name="create_electronic_signature_session_schema",
            )
            if sent_to_persephone is False:
                raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "payload": jwt_mist_session,
        }

    @staticmethod
    async def logout(
        device_jwt_and_thebes_answer_from_request: dict,
    ) -> dict:
        sent_to_persephone = (
            await AuthenticationService.persephone_client.send_to_persephone(
                topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
                partition=PersephoneQueue.USER_LOGOUT.value,
                message=get_user_logout_template_with_data(
                    jwt=device_jwt_and_thebes_answer_from_request["jwt"],
                    unique_id=device_jwt_and_thebes_answer_from_request["jwt_user"][
                        "unique_id"
                    ],
                    device_information=device_jwt_and_thebes_answer_from_request[
                        "device_information"
                    ],
                ),
                schema_name="user_logout_schema",
            )
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "message_key": "email.logout"}

    @staticmethod
    async def _dtvm_client_has_us_trade_allowed(
        user: dict, dw_service=DriveWealthService
    ) -> dict:
        user_dw_status_from_database = user.get("dw")
        if user_dw_status_from_database is None:
            return {}

        client_map_requirements_to_allow_us_trade_from_database = (
            AuthenticationService._get_client_map_requirements_to_allow_us_trade(
                user_dw_status_from_database=user_dw_status_from_database
            )
        )
        if (
            user_dw_status_from_database is not None
            and user_dw_status_from_database != KycStatus.KYC_APPROVED.value
        ):
            user_dw_id = user["portfolios"]["default"].get("us", {}).get("dw_id")
            kyc_status_from_dw = await dw_service.validate_kyc_status(
                user_dw_id=user_dw_id
            )
            AuthenticationService._update_client_has_trade_us_allowed_status_with_dw_status_response(
                client_map_requirements_to_allow_trade_from_database=client_map_requirements_to_allow_us_trade_from_database,
                user_dw_status_from_database=user_dw_status_from_database,
                user_dw_status_from_check_status_request=kyc_status_from_dw,
            )
        return client_map_requirements_to_allow_us_trade_from_database

    @staticmethod
    async def _dtvm_client_has_br_trade_allowed(
        user: dict, solutiontech=Solutiontech
    ) -> dict:
        user_solutiontech_status_from_database = user.get("solutiontech")
        user_sincad_status_from_database = user.get("sincad")
        user_sinacor_account_block_status_from_database = user.get(
            "sinacor_account_block_status"
        )
        user_sinacor_status_from_database = user.get("sinacor")
        user_bmf_account_from_database = (
            user.get("portfolios", {})
            .get("default", {})
            .get("br", {})
            .get("bmf_account")
        )
        user_cpf_from_database = user.get("identifier_document", {}).get("cpf")

        if all(
            [
                user_solutiontech_status_from_database is None,
                user_sincad_status_from_database is None,
                user_sinacor_status_from_database is None,
                user_bmf_account_from_database is None,
            ]
        ):
            return {}

        client_map_requirements_to_allow_br_trade_from_database = AuthenticationService._get_client_map_requirements_to_allow_br_trade(
            user_solutiontech_status_from_database=user_solutiontech_status_from_database,
            user_sincad_status_from_database=user_sincad_status_from_database,
            user_sinacor_status_from_database=user_sinacor_status_from_database,
            user_sinacor_account_block_status_from_database=user_sinacor_account_block_status_from_database,
        )

        user_solutiontech_status_is_synced = (
            user.get("solutiontech") == SolutiontechClientImportStatus.SYNC.value
        )
        if not user_solutiontech_status_is_synced:
            if user.get("solutiontech") == SolutiontechClientImportStatus.FAILED.value:
                await solutiontech.request_client_sync(
                    user_bmf_code=int(user_bmf_account_from_database)
                )
            user_solutiontech_status_from_check_status_request = await solutiontech.check_if_client_is_synced_with_solutiontech(
                user_bmf_code=int(user_bmf_account_from_database),
                user_solutiontech_status_from_database=user_solutiontech_status_from_database,
            )

            client_map_requirements_to_allow_br_trade_from_database = AuthenticationService._update_client_has_trade_allowed_status_with_solutiontech_status_response(
                client_map_requirements_to_allow_trade_from_database=client_map_requirements_to_allow_br_trade_from_database,
                user_solutiontech_status_from_database=user_solutiontech_status_from_database,
                user_solutiontech_status_from_check_status_request=user_solutiontech_status_from_check_status_request,
            )

        user_is_not_already_sync_with_sincad = (
            user_sincad_status_from_database
            is SincadClientImportStatus.NOT_SYNCED.value
        )
        if user_is_not_already_sync_with_sincad:
            sincad_status_from_sinacor = (
                await AuthenticationService._sinacor_is_synced_with_sincad(
                    user_cpf=user_cpf_from_database
                )
            )

            AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
                client_has_trade_allowed_status_with_database_user=client_map_requirements_to_allow_br_trade_from_database,
                sincad_status_from_sinacor=sincad_status_from_sinacor,
                user_sincad_status_from_database=user_sincad_status_from_database,
            )

        sinacor_status_from_sinacor = (
            await AuthenticationService._client_sinacor_status(
                user_cpf=user_cpf_from_database,
                user_bmf_account_from_database=user_bmf_account_from_database,
            )
        )

        client_map_requirements_to_allow_br_trade_from_database = AuthenticationService._update_client_has_trade_allowed_status_with_sinacor_status_response(
            client_has_trade_allowed_status_with_database_user=client_map_requirements_to_allow_br_trade_from_database,
            sinacor_status_from_sinacor=sinacor_status_from_sinacor,
            sinacor_status_from_user_database=user_sinacor_status_from_database,
        )

        sinacor_account_block_status = (
            await AuthenticationService._client_sinacor_is_blocked(
                user_cpf=user_cpf_from_database,
                user_bmf_account_from_database=user_bmf_account_from_database,
            )
        )

        client_map_requirements_to_allow_br_trade_from_database = AuthenticationService._update_client_has_trade_allowed_status_with_sinacor_account_block_status_response(
            client_has_trade_allowed_status_with_database_user=client_map_requirements_to_allow_br_trade_from_database,
            sinacor_account_block_status_from_sinacor=sinacor_account_block_status,
            sinacor_account_block_status_from_user_database=user_sinacor_account_block_status_from_database,
        )

        return client_map_requirements_to_allow_br_trade_from_database

    @staticmethod
    def _get_client_map_requirements_to_allow_br_trade(
        user_solutiontech_status_from_database: str,
        user_sincad_status_from_database: bool,
        user_sinacor_status_from_database: bool,
        user_sinacor_account_block_status_from_database: bool,
    ):
        client_has_trade_allowed_status_with_database_user = {
            "solutiontech": {
                "status": user_solutiontech_status_from_database,
                "status_changed": False,
            },
            "sincad": {
                "status": user_sincad_status_from_database,
                "status_changed": False,
            },
            "sinacor": {
                "status": user_sinacor_status_from_database,
                "status_changed": False,
            },
            "sinacor_account_block_status": {
                "status": user_sinacor_account_block_status_from_database,
                "status_changed": False,
            },
        }

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _get_client_map_requirements_to_allow_us_trade(
        user_dw_status_from_database: bool,
    ):
        client_has_trade_allowed_status_with_database_user = {
            "dw": {
                "status": user_dw_status_from_database,
                "status_changed": False,
            }
        }

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_us_allowed_status_with_dw_status_response(
        client_map_requirements_to_allow_trade_from_database: dict,
        user_dw_status_from_database: str,
        user_dw_status_from_check_status_request: str,
    ):

        dw_status_changed = (
            user_dw_status_from_database != user_dw_status_from_check_status_request
        )

        client_map_requirements_to_allow_trade_from_database["dw"][
            "status"
        ] = user_dw_status_from_check_status_request
        client_map_requirements_to_allow_trade_from_database["dw"][
            "status_changed"
        ] = dw_status_changed

        return client_map_requirements_to_allow_trade_from_database

    @staticmethod
    def _update_client_has_trade_allowed_status_with_solutiontech_status_response(
        client_map_requirements_to_allow_trade_from_database: dict,
        user_solutiontech_status_from_database: str,
        user_solutiontech_status_from_check_status_request: str,
    ):

        solutiontech_status_changed = (
            user_solutiontech_status_from_database
            != user_solutiontech_status_from_check_status_request
        )

        client_map_requirements_to_allow_trade_from_database["solutiontech"][
            "status"
        ] = user_solutiontech_status_from_check_status_request
        client_map_requirements_to_allow_trade_from_database["solutiontech"][
            "status_changed"
        ] = solutiontech_status_changed

        return client_map_requirements_to_allow_trade_from_database

    @staticmethod
    def _update_client_has_trade_allowed_status_with_sincad_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        sincad_status_from_sinacor: bool,
        user_sincad_status_from_database: bool,
    ):

        sincad_status_changed = (
            user_sincad_status_from_database != sincad_status_from_sinacor
        )
        client_has_trade_allowed_status_with_database_user["sincad"][
            "status"
        ] = sincad_status_from_sinacor
        client_has_trade_allowed_status_with_database_user["sincad"][
            "status_changed"
        ] = sincad_status_changed

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_allowed_status_with_sinacor_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        sinacor_status_from_sinacor: bool,
        sinacor_status_from_user_database: bool,
    ):
        sincad_status_changed = (
            sinacor_status_from_user_database != sinacor_status_from_sinacor
        )
        client_has_trade_allowed_status_with_database_user["sinacor"][
            "status"
        ] = sinacor_status_from_sinacor
        client_has_trade_allowed_status_with_database_user["sinacor"][
            "status_changed"
        ] = sincad_status_changed

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_allowed_status_with_sinacor_account_block_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        sinacor_account_block_status_from_sinacor: bool,
        sinacor_account_block_status_from_user_database: bool,
    ):
        sinacor_account_block_status_changed = (
            sinacor_account_block_status_from_sinacor
            != sinacor_account_block_status_from_user_database
        )
        client_has_trade_allowed_status_with_database_user[
            "sinacor_account_block_status"
        ]["status"] = sinacor_account_block_status_from_sinacor
        client_has_trade_allowed_status_with_database_user[
            "sinacor_account_block_status"
        ]["status_changed"] = sinacor_account_block_status_changed

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    async def _sinacor_is_synced_with_sincad(
        user_cpf: int, client_register_repository=ClientRegisterRepository
    ) -> bool:
        sincad_status = await client_register_repository.get_sincad_status(
            user_cpf=user_cpf
        )
        return sincad_status and sincad_status[0] in ["ACE", "ECM"]

    @staticmethod
    async def _client_sinacor_status(
        user_cpf: str,
        user_bmf_account_from_database: str,
        client_register_repository=ClientRegisterRepository,
    ) -> bool:
        sincad_status = await client_register_repository.get_sinacor_status(
            user_cpf=user_cpf, user_bmf_account=user_bmf_account_from_database
        )
        return sincad_status and sincad_status[0] in ["A"]

    @staticmethod
    async def _client_sinacor_is_blocked(
        user_cpf: str,
        user_bmf_account_from_database: str,
        client_register_repository=ClientRegisterRepository,
    ) -> bool:
        sinacor_block_status = (
            await client_register_repository.get_account_sinacor_is_blocked(
                user_cpf=user_cpf, user_bmf_account=user_bmf_account_from_database
            )
        )
        return sinacor_block_status and sinacor_block_status[0] in ["BL"]
